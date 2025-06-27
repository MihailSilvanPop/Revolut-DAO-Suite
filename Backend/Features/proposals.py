import uuid
import hashlib
import time
import pandas as pd
import numpy as np
import re
from Backend.Features.dao_creation import generate_smart_contract_from_summary, compile_solidity_to_bytecode

class Proposal:
    """
    Represents a proposal in the DAO.
    """

    def __init__(self, title, description, proposer, dao):
        """
        Initializes a proposal with the given parameters.

        Args:
            title (str): The title of the proposal.
            description (str): The description of the proposal.
            proposer (str): The proposer of the proposal.
            dao (DAOCreation): The DAO associated with the proposal.
        """
        self.title = title
        self.description = description
        self.proposer = proposer
        self.dao = dao
        self.created_at = int(time.time())
        self.votes = {}  # member: "yes"/"no"
        self.status = "draft"  # draft, active, passed, failed

    def to_string(self):
        """
        Converts the proposal details to a string.

        Returns:
            str: The proposal details as a string.
        """
        return f"Proposal: {self.title}\nDescription: {self.description}\nProposer: {self.proposer}"

def draft_proposal_step_by_step(dao, input_func=input):
    title = input_func("Enter proposal title: ")
    description = input_func("Enter proposal description: ")
    proposer = input_func("Enter proposer name: ")
    return Proposal(title, description, proposer, dao)

def parse_proposal_keywords(proposal_string):
    # Example: look for "increase supply", "change quorum", etc.
    keywords = {
        "increase supply": "increase_supply",
        "change quorum": "change_quorum",
        "set voting time": "set_voting_time",
        "proposal cost": "proposal_cost"
    }
    found = []
    for k, v in keywords.items():
        if k in proposal_string.lower():
            found.append(v)
    return found

def validate_proposal(proposal, dao):
    # Check proposal cost
    cost = dao.governance_rules.get("proposal_cost", 0)
    if dao.wallets.get(proposal.proposer, 0) < cost:
        return False, "Insufficient tokens to submit proposal."
    # Check voting time
    voting_time = dao.governance_rules.get("voting_time_hours", 48) * 3600
    # Check quorum
    quorum = dao.governance_rules.get("quorum", (len(dao.members) // 2) + 1)
    return True, {"cost": cost, "voting_time": voting_time, "quorum": quorum}

def start_voting(proposal):
    """
    Starts the voting process for a proposal.

    Args:
        proposal (Proposal): The proposal to start voting on.
    """
    proposal.status = "active"
    proposal.votes = {}

def cast_vote(proposal, member, vote):
    """
    Casts a vote on a proposal.

    Args:
        proposal (Proposal): The proposal to vote on.
        member (str): The member casting the vote.
        vote (str): The vote ("yes" or "no").

    Returns:
        str: Confirmation message or error message.
    """
    if proposal.status != "active":
        return "Voting not active."
    proposal.votes[member] = vote
    return f"{member} voted {vote}"

def check_voting_result(proposal, dao):
    """
    Checks the result of a proposal's voting process.

    Args:
        proposal (Proposal): The proposal to check.
        dao (DAOCreation): The DAO associated with the proposal.

    Returns:
        str: The result of the voting process.
    """
    # Check voting time
    voting_time = dao.governance_rules.get("voting_time_hours", 48) * 3600
    if int(time.time()) - proposal.created_at > voting_time:
        proposal.status = "failed"
        return "Voting time expired."
    # Check quorum
    quorum = dao.governance_rules.get("quorum", (len(dao.members) // 2) + 1)
    if len(proposal.votes) < quorum:
        proposal.status = "draft"
        return "Quorum not met."
    yes_votes = sum(1 for v in proposal.votes.values() if v == "yes")
    min_votes_to_pass = dao.governance_rules.get("min_votes_to_pass", quorum)
    if yes_votes >= min_votes_to_pass:
        proposal.status = "passed"
        # --- Smart contract generation and blockchain addition ---
        summary = dao.get_summary()
        contract = generate_smart_contract_from_summary(summary)
        bytecode = compile_solidity_to_bytecode(contract)
        dao._add_smart_contract_block(f"Proposal passed and enacted: {proposal.title}")
        return "Proposal passed."
    else:
        proposal.status = "failed"
        return "Proposal failed."