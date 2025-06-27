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
    """
    Executes a token sale transaction for the specified DAO.

    Args:
        dao_id (str): The DAO ID.
        buyer (str): The buyer of the tokens.
        amount (int): The number of tokens to buy.
        token_price (float): The price per token.

    Returns:
        str: Confirmation message or error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = TokenSaleTransaction(dao, buyer, amount, token_price, wallet)
    return tx.execute()

@xl_func("string dao_id, string contributor, int amount: string")
def excel_treasury_contribution(dao_id, contributor, amount):
    """
    Handles a treasury contribution transaction for the specified DAO.

    Args:
        dao_id (str): The DAO ID.
        contributor (str): The contributor.
        amount (int): The contribution amount.

    Returns:
        str: Confirmation message or error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = TreasuryContributionTransaction(dao, contributor, amount, wallet)
    return tx.execute()

@xl_func("string dao_id, string recipient, int amount, string reason: string")
def excel_fund_distribution(dao_id, recipient, amount, reason):
    """
    Distributes funds for the specified DAO.

    Args:
        dao_id (str): The DAO ID.
        recipient (str): The recipient of the funds.
        amount (int): The amount to distribute.
        reason (str): The reason for the distribution.

    Returns:
        str: Confirmation message or error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = FundDistributionTransaction(dao, recipient, amount, reason, wallet)
    return tx.execute()

@xl_func("string dao_id, string target_project, int amount: string")
def excel_investment(dao_id, target_project, amount):
    """
    Executes an investment transaction for the specified DAO.

    Args:
        dao_id (str): The DAO ID.
        target_project (str): The target project for the investment.
        amount (int): The investment amount.

    Returns:
        str: Confirmation message or error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    wallet = excel_wallets.setdefault(dao_id, MultiSigWallet(list(dao.founders), required_signatures=len(dao.founders)))
    tx = InvestmentTransaction(dao, target_project, amount, wallet)
    return tx.execute()

@xl_func("string dao_id: string")
def excel_get_blockchain_info(dao_id):
    """
    Retrieves and displays blockchain information for the specified DAO.

    Args:
        dao_id (str): The DAO ID.

    Returns:
        str: Blockchain information or an error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    return f"Blockchain length: {len(dao.blockchain.chain)}"