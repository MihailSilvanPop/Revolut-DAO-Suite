import unittest
from Backend.Features.dao_creation import DAOCreation
import Frontend.Input.excel_creation as excel

class TestDAOCreationCore(unittest.TestCase):
    def setUp(self):
        self.founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", self.founders, token_name="REVO", initial_supply=900)

    def test_initialization(self):
        self.assertEqual(self.dao.name, "TestDAO")
        self.assertEqual(self.dao.token_name, "REVO")
        self.assertEqual(self.dao.initial_supply, 900)
        self.assertEqual(set(self.dao.founders), set(self.founders))
        self.assertEqual(self.dao.wallets, {f: 300 for f in self.founders})  # 900/3 founders
        print("The test_initialization has passed successfully!")
        print(f"DAO name: {self.dao.name}, Founders: {self.dao.founders}, Token: {self.dao.token_name}, Initial supply: {self.dao.initial_supply}")

    def test_set_governance_rule(self):
        result = self.dao.set_governance_rule("quorum", 2)
        self.assertEqual(result, "Rule 'quorum' set to 2")
        self.assertEqual(self.dao.governance_rules["quorum"], 2)
        print("The test_set_governance_rule has passed successfully!")
        print(f"Governance rules: {self.dao.governance_rules}")

    def test_add_member(self):
        result = self.dao.add_member("Frank")
        self.assertIn("Frank", self.dao.members)
        self.assertEqual(self.dao.wallets["Frank"], 0)
        self.assertEqual(result, "Member 'Frank' added.")
        print("The test_add_member has passed successfully!")
        print(f"Members: {self.dao.members}, Wallets: {self.dao.wallets}")

    def test_create_proposal(self):
        proposal_id = self.dao.create_proposal("Increase Supply", "Proposal to increase REVO supply", "Mihail")
        self.assertEqual(len(self.dao.proposals), 1)
        proposal = self.dao.proposals[0]
        self.assertEqual(proposal["id"], proposal_id)
        self.assertEqual(proposal["title"], "Increase Supply")
        self.assertEqual(proposal["proposer"], "Mihail")
        print("The test_create_proposal has passed successfully!")
        print(f"Proposal: {proposal}")

    def test_vote_on_proposal(self):
        proposal_id = self.dao.create_proposal("Increase Supply", "Proposal to increase REVO supply", "Mihail")
        result = self.dao.vote_on_proposal(proposal_id, "Ben", "yes")
        self.assertEqual(result, f"Ben voted 'yes' on proposal '{proposal_id}'")
        self.assertEqual(self.dao.proposals[0]["votes"]["Ben"], "yes")
        print("The test_vote_on_proposal has passed successfully!")
        print(f"Votes: {self.dao.proposals[0]['votes']}")

    def test_vote_on_proposal_not_found(self):
        result = self.dao.vote_on_proposal("nonexistent_id", "Ben", "yes")
        self.assertEqual(result, "Proposal not found.")
        print("The test_vote_on_proposal_not_found has passed successfully!")
        print(f"Result: {result}")

    def test_get_summary(self):
        summary = self.dao.get_summary()
        self.assertEqual(summary["name"], "TestDAO")
        self.assertEqual(summary["token_name"], "REVO")
        self.assertEqual(set(summary["founders"]), set(self.founders))
        self.assertIn("dao_id", summary)
        self.assertIn("creation_time", summary)
        self.assertIn("members", summary)
        self.assertIn("governance_rules", summary)
        self.assertIn("proposals", summary)
        print("The test_get_summary has passed successfully!")
        print(f"DAO Summary: {summary}")

class TestDAOSmartContractBlocks(unittest.TestCase):
    def setUp(self):
        self.founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", self.founders, token_name="REVO", initial_supply=900)

    def test_blockchain_on_init(self):
        # On init, one block should be present (DAO initialized)
        self.assertEqual(len(self.dao.blockchain.chain), 2)  # genesis + DAO initialized
        last_block = self.dao.blockchain.chain[-1]
        self.assertEqual(last_block.transactions[0]["action"], "DAO initialized")
        print("test_blockchain_on_init passed!")
        print("Last block:", last_block.transactions[0])

    def test_blockchain_on_set_governance_rule(self):
        self.dao.set_governance_rule("quorum", 2)
        self.assertEqual(len(self.dao.blockchain.chain), 3)  # genesis + DAO initialized + rule
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Set governance rule: quorum = 2", last_block.transactions[0]["action"])
        self.assertIn("solidity", last_block.transactions[0])
        self.assertIn("bytecode", last_block.transactions[0])
        print("test_blockchain_on_set_governance_rule passed!")
        print("Last block:", last_block.transactions[0])

    def test_blockchain_on_add_member(self):
        self.dao.add_member("Frank")
        self.assertEqual(len(self.dao.blockchain.chain), 3)  # genesis + DAO initialized + add member
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Added member: Frank", last_block.transactions[0]["action"])
        print("test_blockchain_on_add_member passed!")
        print("Last block:", last_block.transactions[0])

    def test_blockchain_on_create_proposal(self):
        self.dao.create_proposal("Increase Supply", "Proposal to increase REVO supply", "Mihail")
        self.assertEqual(len(self.dao.blockchain.chain), 3)  # genesis + DAO initialized + proposal
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Created proposal: Increase Supply", last_block.transactions[0]["action"])
        print("test_blockchain_on_create_proposal passed!")
        print("Last block:", last_block.transactions[0])

    def test_blockchain_on_vote(self):
        pid = self.dao.create_proposal("Increase Supply", "Proposal to increase REVO supply", "Mihail")
        self.dao.vote_on_proposal(pid, "Ben", "yes")
        self.assertEqual(len(self.dao.blockchain.chain), 4)  # genesis + DAO initialized + proposal + vote
        last_block = self.dao.blockchain.chain[-1]
        self.assertIn("Ben voted 'yes' on proposal", last_block.transactions[0]["action"])
        print("test_blockchain_on_vote passed!")
        print("Last block:", last_block.transactions[0])

if __name__ == "__main__":
    unittest.main()