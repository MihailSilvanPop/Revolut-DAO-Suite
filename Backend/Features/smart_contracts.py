import uuid
import hashlib
import time
import pandas as pd
import numpy as np
import re
from Backend.Database import Block, Blockchain

def parse_governance_rule(input_str):
    """
    Parses a governance rule from user input.

    Args:
        input_str (str): The user input.

    Returns:
        str: The generated Solidity code or None if no rule is recognized.
    """
    if "quorum" in input_str.lower():
        match = re.search(r"(\d+)%\s*\+?\s*(\d*)", input_str)
        if match:
            percent = int(match.group(1))
            plus = int(match.group(2)) if match.group(2) else 0
            return generate_solidity_quorum(percent, plus)
    if "voting time" in input_str.lower():
        match = re.search(r"(\d+)\s*(hours|days|minutes)", input_str)
        if match:
            value = int(match.group(1))
            unit = match.group(2)
            return generate_solidity_voting_time(value, unit)
    if "proposal cost" in input_str.lower():
        match = re.search(r"(\d+)", input_str)
        if match:
            cost = int(match.group(1))
            return generate_solidity_proposal_cost(cost)
    return None

def generate_solidity_quorum(percent, plus):
    """
    Generates Solidity code for quorum rules.

    Args:
        percent (int): The percentage of members required for quorum.
        plus (int): Additional votes required.

    Returns:
        str: The generated Solidity code.
    """
    return f"""
    uint public quorum = (totalMembers * {percent}) / 100 + {plus};
    function isQuorumMet(uint votes) public view returns (bool) {{
        return votes >= quorum;
    }}
    """

def generate_solidity_voting_time(value, unit):
    """
    Generates Solidity code for voting time rules.

    Args:
        value (int): The time value.
        unit (str): The time unit (hours, days, minutes).

    Returns:
        str: The generated Solidity code.
    """
    seconds = value * {"minutes": 60, "hours": 3600, "days": 86400}[unit]
    return f"""
    uint public votingTime = {seconds};
    function getVotingDeadline(uint proposalCreatedAt) public view returns (uint) {{
        return proposalCreatedAt + votingTime;
    }}
    """

def generate_solidity_proposal_cost(cost):
    """
    Generates Solidity code for proposal cost rules.

    Args:
        cost (int): The cost of submitting a proposal.

    Returns:
        str: The generated Solidity code.
    """
    return f"""
    uint public proposalCost = {cost};
    function canSubmitProposal(uint balance) public view returns (bool) {{
        return balance >= proposalCost;
    }}
    """

def compile_solidity_to_bytecode(solidity_code):
    # Simulate compilation (in reality, call solc or use web3.py)
    return f"BYTECODE({hash(solidity_code)})"

def add_contract_to_blockchain(solidity_code, blockchain: Blockchain):
    """
    Adds a smart contract to the blockchain.

    Args:
        solidity_code (str): The Solidity code of the contract.
        blockchain (Blockchain): The blockchain to add the contract to.

    Returns:
        str: The bytecode of the contract.
    """
    bytecode = compile_solidity_to_bytecode(solidity_code)
    tx = {"type": "smart_contract", "solidity": solidity_code, "bytecode": bytecode}
    blockchain.add_block([tx])
    return bytecode

def process_user_input_and_add_contract(user_input, blockchain):
    solidity_code = parse_governance_rule(user_input)
    if not solidity_code:
        return "No recognized governance rule in input."
    bytecode = add_contract_to_blockchain(solidity_code, blockchain)
    return f"Smart contract added to blockchain. Bytecode: {bytecode}"
