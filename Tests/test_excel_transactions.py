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
    """
    Unit tests for Excel-based transaction functions.
    """

    def setUp(self):
        """
        Set up a DAO and clear wallets before each test.
        """
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=1000)
        self.dao_id = self.dao.dao_id
        daos[self.dao_id] = self.dao
        excel_wallets.clear()

    def tearDown(self):
        """
        Clear the global `daos` and `excel_wallets` dictionaries after each test.
        """
        daos.clear()
        excel_wallets.clear()

    def test_excel_token_sale(self):
        """
        Test executing a token sale transaction.
        """
        result = excel_token_sale(self.dao_id, "Alice", 100, 1.5)
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Alice"], 100)
        print("test_excel_token_sale passed.")

    def test_excel_treasury_contribution(self):
        """
        Test executing a treasury contribution transaction.
        """
        self.dao.wallets["Mihail"] = 200  # Give Mihail some tokens
        result = excel_treasury_contribution(self.dao_id, "Mihail", 50)
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Mihail"], 150)
        print("test_excel_treasury_contribution passed.")

    def test_excel_fund_distribution(self):
        """
        Test executing a fund distribution transaction.
        """
        result = excel_fund_distribution(self.dao_id, "Bob", 75, "Grant for project")
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Bob"], 75)
        print("test_excel_fund_distribution passed.")

    def test_excel_investment(self):
        """
        Test executing an investment transaction.
        """
        result = excel_investment(self.dao_id, "CoolProject", 120)
        self.assertIn("executed and recorded on blockchain", result)
        print("test_excel_investment passed.")

    def test_excel_get_blockchain_info(self):
        """
        Test retrieving blockchain information for a DAO.
        """
        excel_token_sale(self.dao_id, "Alice", 100, 1.5)  # Trigger a transaction
        info = excel_get_blockchain_info(self.dao_id)
        self.assertIn("Blockchain length:", info)
        print("test_excel_get_blockchain_info passed.")

    def test_excel_token_sale_dao_not_found(self):
        """
        Test executing a token sale transaction for a non-existent DAO.
        """
        result = excel_token_sale("fake_dao_id", "Alice", 100, 1.5)
        self.assertIn("DAO not found", result)
        print("test_excel_token_sale_dao_not_found passed.")

if __name__ == "__main__":
    unittest.main()