import unittest
import time
from Backend.Features.dao_creation import DAOCreation
from Backend.Features.proposals import (
    Proposal, draft_proposal_step_by_step, parse_proposal_keywords,
    validate_proposal, start_voting, cast_vote, check_voting_result
)

class FakeInput:
    def __init__(self, responses):
        self.responses = responses
        self.index = 0
    def __call__(self, prompt):
        response = self.responses[self.index]
        self.index += 1
        return response

class TestProposalSystem(unittest.TestCase):
    def setUp(self):
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=100)
        self.dao.governance_rules["proposal_cost"] = 10
        self.dao.governance_rules["quorum"] = 2
        self.dao.governance_rules["voting_time_hours"] = 1
        self.dao.governance_rules["min_votes_to_pass"] = 2

    def test_draft_and_parse(self):
        fake_input = FakeInput(["Increase Supply", "We want more tokens", "Mihail"])
        proposal = draft_proposal_step_by_step(self.dao, input_func=fake_input)
        self.assertEqual(proposal.title, "Increase Supply")
        self.assertEqual(proposal.proposer, "Mihail")
        keywords = parse_proposal_keywords(proposal.to_string())
        self.assertIn("increase_supply", keywords)
        print("test_draft_and_parse passed.")

    def test_validate_proposal(self):
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        valid, info = validate_proposal(proposal, self.dao)
        self.assertTrue(valid)
        self.assertEqual(info["cost"], 10)
        print("test_validate_proposal passed.")

    def test_validate_proposal_insufficient_tokens(self):
        proposal = Proposal("Increase Supply", "We want more tokens", "Frank", self.dao)
        valid, msg = validate_proposal(proposal, self.dao)
        self.assertFalse(valid)
        self.assertIn("Insufficient tokens", msg)
        print("test_validate_proposal_insufficient_tokens passed.")

    def test_voting_flow_and_blockchain(self):
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        cast_vote(proposal, "Ben", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "passed")
        self.assertIn("Proposal passed", result)
        # Check that a new smart contract block was added
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Proposal passed and enacted", last_block.transactions[0]["action"])
        self.assertIn("solidity", last_block.transactions[0])
        self.assertIn("bytecode", last_block.transactions[0])
        print("test_voting_flow_and_blockchain passed.")

    def test_voting_quorum_not_met(self):
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "draft")  # Not enough votes to close
        self.assertIn("Quorum not met", result)
        # Blockchain should not change
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len)
        print("test_voting_quorum_not_met passed.")

    def test_voting_time_expired(self):
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        proposal.created_at -= 7200  # 2 hours ago
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        cast_vote(proposal, "Ben", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "failed")
        self.assertIn("Voting time expired", result)
        # Blockchain should not change
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len)
        print("test_voting_time_expired passed.")

if __name__ == "__main__":
    unittest.main()