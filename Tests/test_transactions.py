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
    def setUp(self):
        founders = ["Mihail", "Ben", "Moritz"]
        self.dao = DAOCreation("TestDAO", founders, token_name="REVO", initial_supply=1000)
        self.wallet = MultiSigWallet(owners=founders, required_signatures=3)
        # Give Mihail some tokens for testing
        self.dao.wallets["Mihail"] = 500
        self.dao.wallets["Ben"] = 300
        self.dao.wallets["Moritz"] = 200

    def test_token_sale_transaction(self):
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = TokenSaleTransaction(self.dao, "Alice", 100, 1.5, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Alice"], 100)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertEqual(last_block.transactions[0]["type"], "token_sale")
        print("test_token_sale_transaction passed.")

    def test_treasury_contribution_transaction(self):
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = TreasuryContributionTransaction(self.dao, "Mihail", 50, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Mihail"], 450)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertEqual(last_block.transactions[0]["type"], "treasury_contribution")
        print("test_treasury_contribution_transaction passed.")

    def test_fund_distribution_transaction(self):
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = FundDistributionTransaction(self.dao, "Bob", 75, "Grant for project", self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(self.dao.wallets["Bob"], 75)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertEqual(last_block.transactions[0]["type"], "fund_distribution")
        print("test_fund_distribution_transaction passed.")

    def test_investment_transaction(self):
        prev_chain_len = len(self.dao.blockchain.chain)
        tx = InvestmentTransaction(self.dao, "CoolProject", 120, self.wallet)
        result = tx.execute()
        self.assertIn("executed and recorded on blockchain", result)
        self.assertEqual(len(self.dao.blockchain.chain), prev_chain_len + 1)
        last_block = self.dao.blockchain.chain[-1]
        self.assertEqual(last_block.transactions[0]["type"], "investment")
        print("test_investment_transaction passed.")

    def test_token_sale_transaction_insufficient_signatures(self):
        # Create a wallet that requires all 3 signatures, but only approve with 2
        wallet = MultiSigWallet(owners=["Mihail", "Ben", "Moritz"], required_signatures=3)
        tx = TokenSaleTransaction(self.dao, "Alice", 100, 1.5, wallet)
        # Propose transaction
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
        # Do not approve with "Moritz", so not enough signatures
        with self.assertRaises(Exception):
            wallet.execute_transaction(0)
        print("test_token_sale_transaction_insufficient_signatures passed.")

if __name__ == "__main__":
    unittest.main()