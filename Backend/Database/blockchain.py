import uuid
import hashlib
import time
import pandas as pd
import numpy as np

# --- Blockchain Simulation ---
class Block:
    """
    Represents a single block in the blockchain.
    """

    def __init__(self, index, transactions, previous_hash):
        """
        Initializes a block with the given parameters.

        Args:
            index (int): The index of the block in the chain.
            transactions (list): List of transactions in the block.
            previous_hash (str): The hash of the previous block.
        """
        self.index = index
        self.timestamp = time.time()  # Current timestamp
        self.transactions = transactions  # List of transactions in the block
        self.previous_hash = previous_hash  # Hash of the previous block
        self.hash = self.hash_block()  # Calculate the hash of the block

    def hash_block(self):
        """
        Calculates the hash of the block.

        Returns:
            str: The hash of the block.
        """
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    """
    Represents a blockchain, which is a chain of blocks.
    """

    def __init__(self):
        """
        Initializes the blockchain with a genesis block.
        """
        self.chain = [self.create_genesis_block()]  # Start the chain with the genesis block

    def create_genesis_block(self):
        """
        Creates the genesis block for the blockchain.

        Returns:
            Block: The genesis block.
        """
        return Block(0, [], "0")  # The first block has no transactions and a previous hash of "0"

    def add_block(self, transactions):
        """
        Adds a new block to the blockchain.

        Args:
            transactions (list): List of transactions for the new block.
        """
        previous_block = self.chain[-1]  # Get the last block in the chain
        block = Block(len(self.chain), transactions, previous_block.hash)  # Create a new block
        self.chain.append(block)  # Add the new block to the chain

    def get_chain(self):
        """
        Retrieves the entire blockchain.

        Returns:
            list: A list of dictionaries representing the blocks in the chain.
        """
        return [vars(block) for block in self.chain]  # Convert each block to a dictionary


class MultiSigWallet:
    """
    Represents a multisignature wallet for transaction approvals.
    """

    def __init__(self, owners, required_signatures):
        """
        Initializes the multisig wallet with the given owners and required signatures.

        Args:
            owners (list): List of wallet owners.
            required_signatures (int): Number of required approvals for a transaction.
        """
        self.owners = set(owners)  # Set of wallet owners
        self.required_signatures = required_signatures  # Number of required approvals
        self.pending_transactions = []  # List of pending transactions

    def propose_transaction(self, transaction):
        """
        Proposes a new transaction to the wallet.

        Args:
            transaction (dict): The transaction to propose.
        """
        self.pending_transactions.append({
            "transaction": transaction,  # The transaction details
            "approvals": set()  # Set of owners who have approved the transaction
        })

    def approve_transaction(self, transaction_index, owner):
        """
        Approves a transaction by an owner.

        Args:
            transaction_index (int): The index of the transaction in the pending list.
            owner (str): The owner approving the transaction.

        Returns:
            bool: True if the transaction has enough approvals, False otherwise.
        """
        tx = self.pending_transactions[transaction_index]  # Get the transaction
        if owner in self.owners:  # Check if the owner is valid
            tx["approvals"].add(owner)  # Add the owner's approval
        return len(tx["approvals"]) >= self.required_signatures  # Check if approvals meet the requirement

    def execute_transaction(self, transaction_index):
        """
        Executes a transaction if it has enough approvals.

        Args:
            transaction_index (int): The index of the transaction in the pending list.

        Returns:
            dict: The executed transaction.

        Raises:
            Exception: If the transaction does not have enough approvals.
        """
        tx = self.pending_transactions[transaction_index]  # Get the transaction
        if len(tx["approvals"]) >= self.required_signatures:  # Check if approvals meet the requirement
            return tx["transaction"]  # Return the transaction details
        else:
            raise Exception("Not enough approvals")  # Raise an exception if approvals are insufficient