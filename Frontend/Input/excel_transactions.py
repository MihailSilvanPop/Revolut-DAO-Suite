from pyxll import xl_func
from Backend.Features.transactions import (
    TokenSaleTransaction, TreasuryContributionTransaction,
    FundDistributionTransaction, InvestmentTransaction
)
from Backend.Database.blockchain import MultiSigWallet
from Frontend.Input.excel_creation import daos

# Store multisig wallets by DAO
excel_wallets = {}

@xl_func("string dao_id, string buyer, int amount, float token_price: string")
def excel_token_sale(dao_id, buyer, amount, token_price):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    # Get or create multisig wallet for this DAO
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = TokenSaleTransaction(dao, buyer, amount, token_price, wallet)
    return tx.execute()

@xl_func("string dao_id, string contributor, int amount: string")
def excel_treasury_contribution(dao_id, contributor, amount):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = TreasuryContributionTransaction(dao, contributor, amount, wallet)
    return tx.execute()

@xl_func("string dao_id, string recipient, int amount, string reason: string")
def excel_fund_distribution(dao_id, recipient, amount, reason):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = FundDistributionTransaction(dao, recipient, amount, reason, wallet)
    return tx.execute()

@xl_func("string dao_id, string target_project, int amount: string")
def excel_investment(dao_id, target_project, amount):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = InvestmentTransaction(dao, target_project, amount, wallet)
    return tx.execute()

@xl_func("string dao_id: string")
def excel_get_blockchain_info(dao_id):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    return f"Blockchain length: {len(dao.blockchain.chain)}"