import unittest
from Backend.Features.dao_creation import DAOCreation
from Frontend.Input.excel_transactions import (
    excel_token_sale,
    excel_treasury_contribution,
    excel_fund_distribution,
    excel_investment,
    excel_get_blockchain_info,
    excel_wallets
)
from Frontend.Input.excel_creation import daos

class TestExcelTransactions(unittest.TestCase):
    def setUp(self):
        # Setup a DAO and add it to the global daos dict
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=1000)
        self.dao_id = self.dao.dao_id
        daos[self.dao_id] = self.dao
        # Ensure wallets are clear for each test
        excel_wallets.clear()

    def tearDown(self):
        daos.clear()
        excel_wallets.clear()

    def test_excel_token_sale(self):
        result = excel_token_sale(self.dao_id, "Alice", 100, 1.5)
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Alice"], 100)
        print("test_excel_token_sale passed.")

    def test_excel_treasury_contribution(self):
        # Give Mihail some tokens for contribution
        self.dao.wallets["Mihail"] = 200
        result = excel_treasury_contribution(self.dao_id, "Mihail", 50)
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Mihail"], 150)
        print("test_excel_treasury_contribution passed.")

    def test_excel_fund_distribution(self):
        result = excel_fund_distribution(self.dao_id, "Bob", 75, "Grant for project")
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Bob"], 75)
        print("test_excel_fund_distribution passed.")

    def test_excel_investment(self):
        result = excel_investment(self.dao_id, "CoolProject", 120)
        self.assertIn("executed and recorded on blockchain", result)
        print("test_excel_investment passed.")

    def test_excel_get_blockchain_info(self):
        # Trigger a transaction to add a block
        excel_token_sale(self.dao_id, "Alice", 100, 1.5)
        info = excel_get_blockchain_info(self.dao_id)
        self.assertIn("Blockchain length:", info)
        print("test_excel_get_blockchain_info passed.")

    def test_excel_token_sale_dao_not_found(self):
        result = excel_token_sale("fake_dao_id", "Alice", 100, 1.5)
        self.assertIn("DAO not found", result)
        print("test_excel_token_sale_dao_not_found passed.")

if __name__ == "__main__":
    unittest.main()