import unittest
from Backend.Features.dao_creation import DAOCreation
from Backend.Database.blockchain import MultiSigWallet
from Backend.Features.transactions import (
    TokenSaleTransaction,
    TreasuryContributionTransaction,
    FundDistributionTransaction,
    InvestmentTransaction
)
import time

class TestTransactions(unittest.TestCase):
    """
    Unit tests for DAO transaction types.
    """

    def setUp(self):
        """
        Set up a DAO and multisig wallet for testing.
        """
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=1000)
        self.wallet = MultiSigWallet(owners=founders, required_signatures=3)
        self.dao.wallets["Mihail"] = 500
        self.dao.wallets["Ben"] = 300
        self.dao.wallets["Moritz"] = 200

    def test_token_sale_transaction(self):
        """
        Test executing a token sale transaction.
        """
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = TokenSaleTransaction(self.dao, "Alice", 100, 1.5, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Alice"], 100)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        print("test_token_sale_transaction passed.")

    def test_treasury_contribution_transaction(self):
        """
        Test executing a treasury contribution transaction.
        """
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = TreasuryContributionTransaction(self.dao, "Mihail", 50, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Mihail"], 450)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        print("test_treasury_contribution_transaction passed.")

    def test_fund_distribution_transaction(self):
        """
        Test executing a fund distribution transaction.
        """
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = FundDistributionTransaction(self.dao, "Bob", 75, "Grant for project", self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Bob"], 75)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        print("test_fund_distribution_transaction passed.")

    def test_investment_transaction(self):
        """
        Test executing an investment transaction.
        """
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = InvestmentTransaction(self.dao, "CoolProject", 120, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        print("test_investment_transaction passed.")

    def test_token_sale_transaction_insufficient_signatures(self):
        """
        Test executing a token sale transaction with insufficient signatures.
        """
        wallet = MultiSigWallet(owners=["Mihail", "Ben", "Moritz"], required_signatures=3)
        tx = TokenSaleTransaction(self.dao, "Alice", 100, 1.5, wallet)
        tx_data = {
            "type": "token_sale",
            "buyer": "Alice",
            "amount": 100,
            "token_price": 1.5,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        wallet.propose_transaction(tx_data)
        wallet.approve_transaction(0, "Mihail")
        wallet.approve_transaction(0, "Ben")
        with self.assertRaises(Exception):
            wallet.execute_transaction(0)
        print("test_token_sale_transaction_insufficient_signatures passed.")

if __name__ == "__main__":
    unittest.main()