from pyxll import xl_func
from Backend.Database import Blockchain
from Backend.Features.smart_contracts import process_user_input_and_add_contract

# Optionally, store blockchains by DAO or session if needed
excel_blockchains = {}

@xl_func("string session_id, string contract_string: string")
def excel_add_smart_contract(session_id, contract_string):
    """
    Adds a smart contract to the blockchain for the given session.

    Args:
        session_id (str): The session or DAO id.
        contract_string (str): The contract description, e.g. "Set voting time to maximum 24 hours".

    Returns:
        str: Result message.
    """
    # Get or create a blockchain for this session/DAO
    bc = excel_blockchains.setdefault(session_id, Blockchain())
    result = process_user_input_and_add_contract(contract_string, bc)
    return result

@xl_func("string session_id: string")
def excel_get_smart_contracts(session_id):
    """
    Returns a summary of smart contracts on the blockchain for the given session.

    Args:
        session_id (str): The session or DAO id.

    Returns:
        str: Summary of contracts.
    """
    bc = excel_blockchains.get(session_id)
    if not bc:
        return "No blockchain found for this session."
    contracts = []
    for block in bc.chain:
        for tx in block.transactions:
            if tx.get("type") == "smart_contract":
                contracts.append(tx.get("action", str(tx)))
    if not contracts:
        return "No smart contracts found."
    return "\n".join(contracts)