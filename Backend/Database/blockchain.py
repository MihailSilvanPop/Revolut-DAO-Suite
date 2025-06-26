import uuid
import hashlib
import time
import pandas as pd
import numpy as np

# --- Blockchain Simulation ---
class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.timestamp = time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.hash = self.hash_block()

    def hash_block(self):
        block_string = f"{self.index}{self.timestamp}{self.transactions}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, [], "0")

    def add_block(self, transactions):
        previous_block = self.chain[-1]
        block = Block(len(self.chain), transactions, previous_block.hash)
        self.chain.append(block)

    def get_chain(self):
        return [vars(block) for block in self.chain]
    
class MultiSigWallet:
    def __init__(self, owners, required_signatures):
        self.owners = set(owners)
        self.required_signatures = required_signatures
        self.pending_transactions = []

    def propose_transaction(self, transaction):
        self.pending_transactions.append({
            "transaction": transaction,
            "approvals": set()
        })

    def approve_transaction(self, transaction_index, owner):
        tx = self.pending_transactions[transaction_index]
        if owner in self.owners:
            tx["approvals"].add(owner)
        return len(tx["approvals"]) >= self.required_signatures

    def execute_transaction(self, transaction_index):
        tx = self.pending_transactions[transaction_index]
        if len(tx["approvals"]) >= self.required_signatures:
            return tx["transaction"]
        else:
            raise Exception("Not enough approvals")