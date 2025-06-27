import unittest
from Backend.Database import Block, Blockchain, MultiSigWallet

# --- Unit Tests for Blockchain ---
class TestBlockchain(unittest.TestCase):
    """
    Unit tests for the Blockchain and MultiSigWallet classes.
    """

    def test_block_creation(self):
        """
        Test the creation of a block with valid transactions and a previous hash.
        """
        previous_hash = "0000000000000000000a7b3c6d8e9f1234567890abcdef1234567890abcdef12"
        transactions = [
            {"from": "alice", "to": "bob", "amount": 1500, "token": "REVO", "timestamp": "2024-06-26T12:00:00Z"}
        ]
        block = Block(1, transactions, previous_hash)
        self.assertEqual(block.index, 1)
        self.assertEqual(block.transactions, transactions)
        self.assertEqual(block.previous_hash, previous_hash)
        self.assertIsInstance(block.hash, str)
        print("The test_block_creation has passed successfully!")

    def test_block_hash_uniqueness(self):
        """
        Test that blocks with different transactions produce unique hashes.
        """
        previous_hash = "0000000000000000000a7b3c6d8e9f1234567890abcdef1234567890abcdef12"
        transactions1 = [
            {"from": "alice", "to": "bob", "amount": 1500, "token": "REVO", "timestamp": "2024-06-26T12:00:00Z"}
        ]
        transactions2 = [
            {"from": "carol", "to": "dave", "amount": 250, "token": "REVO", "timestamp": "2024-06-26T12:05:00Z"}
        ]
        block1 = Block(1, transactions1, previous_hash)
        block2 = Block(1, transactions2, previous_hash)
        self.assertNotEqual(block1.hash, block2.hash)
        print("The test_block_hash_uniqueness has passed successfully!")

    def test_blockchain_genesis_block(self):
        """
        Test that the blockchain initializes with a valid genesis block.
        """
        bc = Blockchain()
        self.assertEqual(len(bc.chain), 1)
        self.assertEqual(bc.chain[0].index, 0)
        self.assertEqual(bc.chain[0].previous_hash, "0")
        print("The test_blockchain_genesis_block has passed successfully!")

    def test_blockchain_add_block(self):
        """
        Test adding a new block to the blockchain.
        """
        bc = Blockchain()
        transactions = [
            {"from": "eve", "to": "frank", "amount": 500, "token": "REVO", "timestamp": "2024-06-26T12:10:00Z"}
        ]
        bc.add_block(transactions)
        self.assertEqual(len(bc.chain), 2)
        self.assertEqual(bc.chain[1].transactions, transactions)
        self.assertEqual(bc.chain[1].previous_hash, bc.chain[0].hash)
        print("The test_blockchain_add_block has passed successfully!")

    def test_blockchain_chain_structure(self):
        """
        Test the structure of the blockchain after adding multiple blocks.
        """
        bc = Blockchain()
        tx1 = [{"from": "alice", "to": "bob", "amount": 1500, "token": "REVO", "timestamp": "2024-06-26T12:00:00Z"}]
        tx2 = [{"from": "carol", "to": "dave", "amount": 250, "token": "REVO", "timestamp": "2024-06-26T12:05:00Z"}]
        bc.add_block(tx1)
        bc.add_block(tx2)
        chain = bc.get_chain()
        self.assertIsInstance(chain, list)
        self.assertTrue(all("hash" in block for block in chain))
        self.assertEqual(chain[1]['transactions'], tx1)
        self.assertEqual(chain[2]['transactions'], tx2)
        print("The test_blockchain_chain_structure has passed successfully!")

    def test_multisig_wallet(self):
        """
        Test the functionality of the MultiSigWallet class, including proposing,
        approving, and executing transactions.
        """
        owners = ["alice", "bob", "carol"]
        wallet = MultiSigWallet(owners, required_signatures=2)
        tx = {"from": "alice", "to": "dave", "amount": 1000, "token": "REVO", "timestamp": "2024-06-26T13:00:00Z"}
        wallet.propose_transaction(tx)
        # Only one approval, should not execute
        self.assertFalse(wallet.approve_transaction(0, "alice"))
        # Second approval, should now be executable
        self.assertTrue(wallet.approve_transaction(0, "bob"))
        # Now execute
        executed_tx = wallet.execute_transaction(0)
        self.assertEqual(executed_tx, tx)
        print("The test_multisig_wallet has passed successfully!")

if __name__ == "__main__":
    unittest.main()