import unittest
import time
from Backend.Features.dao_creation import DAOCreation
from Backend.Features.proposals import (
    Proposal, draft_proposal_step_by_step, parse_proposal_keywords,
    validate_proposal, start_voting, cast_vote, check_voting_result
)

class FakeInput:
    """
    A mock input class to simulate user input for testing.
    """

    def __init__(self, responses):
        """
        Initialize the mock input with a list of responses.

        Args:
            responses (list): List of responses to simulate user input.
        """
        self.responses = responses
        self.index = 0

    def __call__(self, prompt):
        """
        Simulate user input by returning the next response.

        Args:
            prompt (str): The prompt to display (ignored in this mock).

        Returns:
            str: The next response from the list.
        """
        response = self.responses[self.index]
        self.index += 1
        return response

class TestProposalSystem(unittest.TestCase):
    """
    Unit tests for the DAO proposal system.
    """

    def setUp(self):
        """
        Set up a DAO instance with governance rules for testing.
        """
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=100)
        self.dao.governance_rules["proposal_cost"] = 10
        self.dao.governance_rules["quorum"] = 2
        self.dao.governance_rules["voting_time_hours"] = 1
        self.dao.governance_rules["min_votes_to_pass"] = 2

    def test_draft_and_parse(self):
        """
        Test drafting a proposal and parsing its keywords.
        """
        fake_input = FakeInput(["Increase Supply", "We want more tokens", "Mihail"])
        proposal = draft_proposal_step_by_step(self.dao, input_func=fake_input)
        self.assertEqual(proposal.title, "Increase Supply")
        self.assertEqual(proposal.proposer, "Mihail")
        keywords = parse_proposal_keywords(proposal.to_string())
        self.assertIn("increase_supply", keywords)
        print("test_draft_and_parse passed.")

    def test_validate_proposal(self):
        """
        Test validating a proposal with sufficient tokens.
        """
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        valid, info = validate_proposal(proposal, self.dao)
        self.assertTrue(valid)
        self.assertEqual(info["cost"], 10)
        print("test_validate_proposal passed.")

    def test_validate_proposal_insufficient_tokens(self):
        """
        Test validating a proposal with insufficient tokens.
        """
        proposal = Proposal("Increase Supply", "We want more tokens", "Frank", self.dao)
        valid, msg = validate_proposal(proposal, self.dao)
        self.assertFalse(valid)
        self.assertIn("Insufficient tokens", msg)
        print("test_validate_proposal_insufficient_tokens passed.")

    def test_voting_flow_and_blockchain(self):
        """
        Test the voting process and its effect on the blockchain.
        """
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        cast_vote(proposal, "Ben", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "passed")
        self.assertIn("Proposal passed", result)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Proposal passed and enacted", last_block.transactions[0]["action"])
        print("test_voting_flow_and_blockchain passed.")

    def test_voting_quorum_not_met(self):
        """
        Test the scenario where a proposal does not meet the quorum requirement.
        """
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "draft")
        self.assertIn("Quorum not met", result)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len)
        print("test_voting_quorum_not_met passed.")

    def test_voting_time_expired(self):
        """
        Test the scenario where the voting time has expired.
        """
        proposal = Proposal("Increase Supply", "We want more tokens", "Mihail", self.dao)
        proposal.created_at -= 7200  # 2 hours ago
        start_voting(proposal)
        cast_vote(proposal, "Mihail", "yes")
        cast_vote(proposal, "Ben", "yes")
        prev_chain_len = len(self.dao.blockchain.chain)
        result = check_voting_result(proposal, self.dao)
        self.assertEqual(proposal.status, "failed")
        self.assertIn("Voting time expired", result)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len)
        print("test_voting_time_expired passed.")

if __name__ == "__main__":
    unittest.main()