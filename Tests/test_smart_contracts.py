from Backend.Database import Blockchain
from Backend.Features.smart_contracts import process_user_input_and_add_contract
import unittest

class TestSmartContracts(unittest.TestCase):
    def test_quorum_smart_contract(self):
        bc = Blockchain()
        result = process_user_input_and_add_contract("Set quorum to 50% +1", bc)
        print(result)
        self.assertIn("Smart contract added to blockchain", result)
        self.assertEqual(len(bc.chain), 2)
        self.assertEqual(bc.chain[1].transactions[0]["type"], "smart_contract")

    def test_voting_time_smart_contract(self):
        bc = Blockchain()
        result = process_user_input_and_add_contract("Set voting time to 48 hours", bc)
        print(result)
        self.assertIn("Smart contract added to blockchain", result)
        self.assertEqual(len(bc.chain), 2)
        self.assertEqual(bc.chain[1].transactions[0]["type"], "smart_contract")

    def test_proposal_cost_smart_contract(self):
        bc = Blockchain()
        result = process_user_input_and_add_contract("Set proposal cost to 10", bc)
        print(result)
        self.assertIn("Smart contract added to blockchain", result)
        self.assertEqual(len(bc.chain), 2)
        self.assertEqual(bc.chain[1].transactions[0]["type"], "smart_contract")

    def test_unrecognized_input(self):
        bc = Blockchain()
        result = process_user_input_and_add_contract("This is not a governance rule", bc)
        print(result)
        self.assertIn("No recognized governance rule in input.", result)
        self.assertEqual(len(bc.chain), 1)  # Only genesis block

if __name__ == "__main__":
    unittest.main()