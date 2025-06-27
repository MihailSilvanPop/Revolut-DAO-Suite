import uuid
import hashlib
import time
import pandas as pd
import numpy as np
from Backend.Database.blockchain import MultiSigWallet
from Backend.Features.dao_creation import generate_smart_contract_from_summary, compile_solidity_to_bytecode

class TokenSaleTransaction:
    """
    Represents a token sale transaction for a DAO.
    """

    def __init__(self, dao, buyer, amount, token_price, multisig_wallet: MultiSigWallet):
        """
        Initializes the token sale transaction.

        Args:
            dao: The DAO object associated with the transaction.
            buyer: The buyer of the tokens.
            amount: The number of tokens to buy.
            token_price: The price per token.
            multisig_wallet: The multisig wallet used for transaction approvals.
        """
        self.dao = dao
        self.buyer = buyer
        self.amount = amount  # Number of tokens to buy
        self.token_price = token_price  # Price per token in ETH or other currency
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.multisig_wallet = multisig_wallet

    def execute(self):
        """
        Executes the token sale transaction.

        Returns:
            str: A message indicating the success or failure of the transaction.
        """
        tx_data = {
            "type": "token_sale",
            "buyer": self.buyer,
            "amount": self.amount,
            "token_price": self.token_price,
            "timestamp": self.timestamp
        }
        # Propose the transaction to the multisig wallet
        self.multisig_wallet.propose_transaction(tx_data)
        # Simulate approvals (in real use, call approve_transaction for each owner)
        for owner in self.multisig_wallet.owners:
            self.multisig_wallet.approve_transaction(0, owner)
        if self.multisig_wallet.execute_transaction(0):
            # Update DAO wallets and treasury
            self.dao.wallets[self.buyer] = self.dao.wallets.get(self.buyer, 0) + self.amount
            # Generate and record smart contract
            summary = self.dao.get_summary()
            contract = generate_smart_contract_from_summary(summary)
            bytecode = compile_solidity_to_bytecode(contract)
            self.dao.blockchain.add_block([{
                "type": "token_sale",
                "buyer": self.buyer,
                "amount": self.amount,
                "token_price": self.token_price,
                "solidity": contract,
                "bytecode": bytecode,
                "timestamp": self.timestamp
            }])
            return "Token sale executed and recorded on blockchain."
        return "Token sale failed multisig approval."

class TreasuryContributionTransaction:
    """
    Represents a treasury contribution transaction for a DAO.
    """

    def __init__(self, dao, contributor, amount, multisig_wallet: MultiSigWallet):
        """
        Initializes the treasury contribution transaction.

        Args:
            dao: The DAO object associated with the transaction.
            contributor: The contributor making the contribution.
            amount: The amount contributed to the treasury.
            multisig_wallet: The multisig wallet used for transaction approvals.
        """
        self.dao = dao
        self.contributor = contributor
        self.amount = amount
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.multisig_wallet = multisig_wallet

    def execute(self):
        """
        Executes the treasury contribution transaction.

        Returns:
            str: A message indicating the success or failure of the transaction.
        """
        tx_data = {
            "type": "treasury_contribution",
            "contributor": self.contributor,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        # Propose the transaction to the multisig wallet
        self.multisig_wallet.propose_transaction(tx_data)
        for owner in self.multisig_wallet.owners:
            self.multisig_wallet.approve_transaction(0, owner)
        if self.multisig_wallet.execute_transaction(0):
            # Update DAO treasury (could be a field in DAO)
            self.dao.wallets[self.contributor] = self.dao.wallets.get(self.contributor, 0) - self.amount
            # Generate and record smart contract
            summary = self.dao.get_summary()
            contract = generate_smart_contract_from_summary(summary)
            bytecode = compile_solidity_to_bytecode(contract)
            self.dao.blockchain.add_block([{
                "type": "treasury_contribution",
                "contributor": self.contributor,
                "amount": self.amount,
                "solidity": contract,
                "bytecode": bytecode,
                "timestamp": self.timestamp
            }])
            return "Treasury contribution executed and recorded on blockchain."
        return "Treasury contribution failed multisig approval."

class FundDistributionTransaction:
    """
    Represents a fund distribution transaction for a DAO.
    """

    def __init__(self, dao, recipient, amount, reason, multisig_wallet: MultiSigWallet):
        """
        Initializes the fund distribution transaction.

        Args:
            dao: The DAO object associated with the transaction.
            recipient: The recipient of the funds.
            amount: The amount to distribute.
            reason: The reason for the fund distribution.
            multisig_wallet: The multisig wallet used for transaction approvals.
        """
        self.dao = dao
        self.recipient = recipient
        self.amount = amount
        self.reason = reason
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.multisig_wallet = multisig_wallet

    def execute(self):
        """
        Executes the fund distribution transaction.

        Returns:
            str: A message indicating the success or failure of the transaction.
        """
        tx_data = {
            "type": "fund_distribution",
            "recipient": self.recipient,
            "amount": self.amount,
            "reason": self.reason,
            "timestamp": self.timestamp
        }
        # Propose the transaction to the multisig wallet
        self.multisig_wallet.propose_transaction(tx_data)
        for owner in self.multisig_wallet.owners:
            self.multisig_wallet.approve_transaction(0, owner)
        if self.multisig_wallet.execute_transaction(0):
            # Update DAO wallets
            self.dao.wallets[self.recipient] = self.dao.wallets.get(self.recipient, 0) + self.amount
            # Generate and record smart contract
            summary = self.dao.get_summary()
            contract = generate_smart_contract_from_summary(summary)
            bytecode = compile_solidity_to_bytecode(contract)
            self.dao.blockchain.add_block([{
                "type": "fund_distribution",
                "recipient": self.recipient,
                "amount": self.amount,
                "reason": self.reason,
                "solidity": contract,
                "bytecode": bytecode,
                "timestamp": self.timestamp
            }])
            return "Fund distribution executed and recorded on blockchain."
        return "Fund distribution failed multisig approval."

class InvestmentTransaction:
    """
    Represents an investment transaction for a DAO.
    """

    def __init__(self, dao, target_project, amount, multisig_wallet: MultiSigWallet):
        """
        Initializes the investment transaction.

        Args:
            dao: The DAO object associated with the transaction.
            target_project: The target project for the investment.
            amount: The amount to invest.
            multisig_wallet: The multisig wallet used for transaction approvals.
        """
        self.dao = dao
        self.target_project = target_project
        self.amount = amount
        self.timestamp = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.multisig_wallet = multisig_wallet

    def execute(self):
        """
        Executes the investment transaction.

        Returns:
            str: A message indicating the success or failure of the transaction.
        """
        tx_data = {
            "type": "investment",
            "target_project": self.target_project,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
        # Propose the transaction to the multisig wallet
        self.multisig_wallet.propose_transaction(tx_data)
        for owner in self.multisig_wallet.owners:
            self.multisig_wallet.approve_transaction(0, owner)
        if self.multisig_wallet.execute_transaction(0):
            # Generate and record smart contract
            summary = self.dao.get_summary()
            contract = generate_smart_contract_from_summary(summary)
            bytecode = compile_solidity_to_bytecode(contract)
            self.dao.blockchain.add_block([{
                "type": "investment",
                "target_project": self.target_project,
                "amount": self.amount,
                "solidity": contract,
                "bytecode": bytecode,
                "timestamp": self.timestamp
            }])
            return "Investment executed and recorded on blockchain."
        return "Investment failed multisig approval."