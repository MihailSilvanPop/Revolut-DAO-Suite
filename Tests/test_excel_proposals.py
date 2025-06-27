import unittest
from unittest.mock import patch
from Backend.Features.dao_creation import DAOCreation
from Frontend.Input.excel_proposals import (
    excel_create_proposal,
    excel_cast_vote,
    excel_check_proposal_result,
    excel_proposals
)
from Frontend.Input.excel_creation import daos

class TestExcelProposals(unittest.TestCase):
    """
    Unit tests for Excel-based proposal management functions.
    """

    def setUp(self):
        """
        Set up a DAO and add it to the global `daos` dictionary for testing.
        """
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=100)
        self.dao_id = self.dao.dao_id
        daos[self.dao_id] = self.dao
        self.dao.governance_rules["proposal_cost"] = 10
        self.dao.governance_rules["quorum"] = 2
        self.dao.governance_rules["voting_time_hours"] = 1
        self.dao.governance_rules["min_votes_to_pass"] = 2

    def tearDown(self):
        """
        Clear the global `daos` and `excel_proposals` dictionaries after each test.
        """
        daos.clear()
        excel_proposals.clear()

    def test_excel_create_proposal(self):
        """
        Test the creation of a proposal using the `excel_create_proposal` function.
        """
        result = excel_create_proposal(self.dao_id, "Increase Supply", "We want more tokens", "Mihail")
        self.assertIn("Proposal 'Increase Supply' created", result)
        key = f"{self.dao_id}:Increase Supply"
        self.assertIn(key, excel_proposals)
        print("test_excel_create_proposal passed.")

    def test_excel_cast_vote_and_check_result(self):
        """
        Test the voting process and result checking for a proposal.
        """
        # Create a proposal
        excel_create_proposal(self.dao_id, "Increase Supply", "We want more tokens", "Mihail")
        # Cast votes from all 3 founders
        vote_result1 = excel_cast_vote(self.dao_id, "Increase Supply", "Mihail", "yes")
        vote_result2 = excel_cast_vote(self.dao_id, "Increase Supply", "Ben", "yes")
        vote_result3 = excel_cast_vote(self.dao_id, "Increase Supply", "Moritz", "yes")
        # Check the result
        result = excel_check_proposal_result(self.dao_id, "Increase Supply")
        print("Votes:", vote_result1, vote_result2, vote_result3)
        print("Result:", result)
        self.assertIn("Proposal passed", result)
        print("test_excel_cast_vote_and_check_result passed.")

    def test_excel_check_proposal_result_quorum_not_met(self):
        """
        Test the scenario where a proposal does not meet the quorum requirement.
        """
        excel_create_proposal(self.dao_id, "Increase Supply", "We want more tokens", "Mihail")
        excel_cast_vote(self.dao_id, "Increase Supply", "Mihail", "yes")
        result = excel_check_proposal_result(self.dao_id, "Increase Supply")
        self.assertIn("Quorum not met", result)
        print("test_excel_check_proposal_result_quorum_not_met passed.")

    def test_excel_check_proposal_result_proposal_not_found(self):
        """
        Test the scenario where the proposal being checked does not exist.
        """
        result = excel_check_proposal_result(self.dao_id, "Nonexistent Proposal")
        self.assertIn("Proposal not found", result)
        print("test_excel_check_proposal_result_proposal_not_found passed.")

    def test_excel_create_proposal_dao_not_found(self):
        """
        Test the scenario where the DAO for the proposal does not exist.
        """
        result = excel_create_proposal("fake_dao_id", "Test", "Desc", "Mihail")
        self.assertIn("DAO not found", result)
        print("test_excel_create_proposal_dao_not_found passed.")

if __name__ == "__main__":
    unittest.main()