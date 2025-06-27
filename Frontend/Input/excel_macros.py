from pyxll import xl_macro, xl_app
from Frontend.Input.excel_creation import (
    excel_set_dao_name,
    excel_set_num_founders,
    excel_add_founder,
    excel_set_token_and_supply,
    excel_finalize_dao
)
from Frontend.Input.excel_proposals import (
    excel_create_proposal,
    excel_cast_vote,
    excel_check_proposal_result
)
from Frontend.Input.excel_transactions import (
    excel_token_sale,
    excel_treasury_contribution,
    excel_fund_distribution,
    excel_investment,
    excel_get_blockchain_info
)
from Frontend.Input.excel_smart_contracts import (
    excel_add_smart_contract,
    excel_get_smart_contracts,
)

@xl_macro()
def macro_set_dao_name():
    """Set the DAO name using values from Creation!P13 (session_id) and Creation!R13 (name)."""
    app = xl_app()
    session_id = app.Worksheets("Creation").Range("P13").Value
    name = app.Worksheets("Creation").Range("R13").Value
    result = excel_set_dao_name(session_id, name)
    app.Worksheets("Creation").Range("P17").Value = result

@xl_macro()
def macro_set_num_founders():
    """Set the number of founders using Creation!P13 (session_id) and Creation!P20 (num_founders)."""
    app = xl_app()
    session_id = app.Worksheets("Creation").Range("P13").Value
    num_founders = int(app.Worksheets("Creation").Range("P20").Value)
    result = excel_set_num_founders(session_id, num_founders)
    app.Worksheets("Creation").Range("P24").Value = result

@xl_macro()
def macro_add_founder():
    """Add a founder using Creation!P13 (session_id) and Creation!P26 (founder name)."""
    app = xl_app()
    session_id = app.Worksheets("Creation").Range("P13").Value
    founder = app.Worksheets("Creation").Range("P26").Value
    result = excel_add_founder(session_id, founder)
    app.Worksheets("Creation").Range("P30").Value = result

@xl_macro()
def macro_set_token_and_supply():
    """Set the DAO token and initial supply using Creation!P13 (session_id), Creation!P33 (token), Creation!R33 (supply)."""
    app = xl_app()
    session_id = app.Worksheets("Creation").Range("P13").Value
    token_name = app.Worksheets("Creation").Range("P33").Value
    initial_supply = int(app.Worksheets("Creation").Range("R33").Value)
    result = excel_set_token_and_supply(session_id, token_name, initial_supply)
    app.Worksheets("Creation").Range("P37").Value = result

@xl_macro()
def macro_finalize_dao():
    """Finalize DAO creation using Creation!P13 (session_id)."""
    app = xl_app()
    session_id = app.Worksheets("Creation").Range("P13").Value
    result = excel_finalize_dao(session_id)
    app.Worksheets("Creation").Range("P42").Value = result

@xl_macro()
def macro_create_proposal():
    """Create a proposal using Proposal!P12 (dao_id), Proposal!R15 (title), Proposal!P18 (description), Proposal!R16 (proposer)."""
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    title = app.Worksheets("Proposal").Range("R15").Value
    description = app.Worksheets("Proposal").Range("P18").Value
    proposer = app.Worksheets("Proposal").Range("R16").Value
    result = excel_create_proposal(dao_id, title, description, proposer)
    app.Worksheets("Proposal").Range("P22").Value = result

@xl_macro()
def macro_cast_vote():
    """Cast a vote using Proposal!P12 (dao_id), Proposal!R15 (title), Proposal!E14 (member), Proposal!E15 (vote)."""
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    title = app.Worksheets("Proposal").Range("R15").Value
    member = app.Worksheets("Proposal").Range("P25").Value
    vote = app.Worksheets("Proposal").Range("S25").Value
    result = excel_cast_vote(dao_id, title, member, vote)
    app.Worksheets("Proposal").Range("P29").Value = result

@xl_macro()
def macro_check_proposal_result():
    """Check proposal result using Proposal!P12 (dao_id) and Proposal!R15 (title)."""
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    title = app.Worksheets("Proposal").Range("R15").Value
    result = excel_check_proposal_result(dao_id, title)
    app.Worksheets("Proposal").Range("P30").Value = result

@xl_macro()
def macro_add_smart_contract():
    """Add a smart contract using Proposal!P12 (dao_id) and Proposal!E18 (contract string)."""
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    contract_string = app.Worksheets("Proposal").Range("P18").Value
    result = excel_add_smart_contract(dao_id, contract_string)
    app.Worksheets("Proposal").Range("P34").Value = result

@xl_macro()
def macro_get_smart_contracts():
    """
    Get all smart contracts for a DAO.
    Reads DAO ID from Creation!P42 and writes the result to Proposal!V10.
    """
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    result = excel_get_smart_contracts(dao_id)
    app.Worksheets("Proposal").Range("V10").Value = result

@xl_macro()
def macro_token_sale():
    """
    Execute a token sale.
    Reads DAO ID from Creation!P42, buyer from Transactions!R15, amount from Transactions!R16,
    and token price from Transactions!R17. Writes the result to Transactions!P20.
    """
    app = xl_app()
    dao_id = app.Worksheets("Creation").Range("P42").Value
    buyer = app.Worksheets("Transactions").Range("R15").Value
    amount = int(app.Worksheets("Transactions").Range("R16").Value)
    token_price = float(app.Worksheets("Transactions").Range("R17").Value)
    result = excel_token_sale(dao_id, buyer, amount, token_price)
    app.Worksheets("Transactions").Range("P20").Value = result

@xl_macro()
def macro_treasury_contribution():
    """
    Execute a treasury contribution.
    Reads DAO ID from Transactions!D20, contributor from Transactions!E24,
    and amount from Transactions!E25. Writes the result to Transactions!E26.
    """
    app = xl_app()
    dao_id = app.Worksheets("Transactions").Range("D20").Value
    contributor = app.Worksheets("Transactions").Range("E24").Value
    amount = int(app.Worksheets("Transactions").Range("E25").Value)
    result = excel_treasury_contribution(dao_id, contributor, amount)
    app.Worksheets("Transactions").Range("E26").Value = result

@xl_macro()
def macro_fund_distribution():
    """
    Execute a fund distribution.
    Reads DAO ID from Transactions!D20, recipient from Transactions!E27,
    amount from Transactions!E28, and reason from Transactions!E29.
    Writes the result to Transactions!E30.
    """
    app = xl_app()
    dao_id = app.Worksheets("Transactions").Range("D20").Value
    recipient = app.Worksheets("Transactions").Range("E27").Value
    amount = int(app.Worksheets("Transactions").Range("E28").Value)
    reason = app.Worksheets("Transactions").Range("E29").Value
    result = excel_fund_distribution(dao_id, recipient, amount, reason)
    app.Worksheets("Transactions").Range("E30").Value = result

@xl_macro()
def macro_investment():
    """
    Execute an investment.
    Reads DAO ID from Transactions!D20, target project from Transactions!E31,
    and amount from Transactions!E32. Writes the result to Transactions!E33.
    """
    app = xl_app()
    dao_id = app.Worksheets("Transactions").Range("D20").Value
    target_project = app.Worksheets("Transactions").Range("E31").Value
    amount = int(app.Worksheets("Transactions").Range("E32").Value)
    result = excel_investment(dao_id, target_project, amount)
    app.Worksheets("Transactions").Range("E33").Value = result

@xl_macro()
def macro_get_blockchain_info():
    """
    Get blockchain info.
    Reads DAO ID from Transactions!D20 and writes the result to Transactions!E34.
    """
    app = xl_app()
    dao_id = app.Worksheets("Transactions").Range("D20").Value
    result = excel_get_blockchain_info(dao_id)
    app.Worksheets("Transactions").Range("E34").Value = result