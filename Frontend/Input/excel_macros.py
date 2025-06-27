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

@xl_macro()
def macro_set_dao_name():
    app = xl_app()
    session_id = app.Range("D2").Value
    name = app.Range("E2").Value
    result = excel_set_dao_name(session_id, name)
    app.Range("E4").Value = result  # Output below input

@xl_macro()
def macro_set_num_founders():
    app = xl_app()
    session_id = app.Range("D2").Value
    num_founders = int(app.Range("E3").Value)
    result = excel_set_num_founders(session_id, num_founders)
    app.Range("E5").Value = result  # Output below input

@xl_macro()
def macro_add_founder():
    app = xl_app()
    session_id = app.Range("D2").Value
    founder = app.Range("E4").Value
    result = excel_add_founder(session_id, founder)
    app.Range("E6").Value = result  # Output below input

@xl_macro()
def macro_set_token_and_supply():
    app = xl_app()
    session_id = app.Range("D2").Value
    token_name = app.Range("E5").Value
    initial_supply = int(app.Range("E6").Value)
    result = excel_set_token_and_supply(session_id, token_name, initial_supply)
    app.Range("E7").Value = result  # Output below input

@xl_macro()
def macro_finalize_dao():
    app = xl_app()
    session_id = app.Range("D2").Value
    result = excel_finalize_dao(session_id)
    app.Range("E8").Value = result  # Output below input

@xl_macro()
def macro_create_proposal():
    app = xl_app()
    dao_id = app.Range("D10").Value
    title = app.Range("E10").Value
    description = app.Range("E11").Value
    proposer = app.Range("E12").Value
    result = excel_create_proposal(dao_id, title, description, proposer)
    app.Range("E13").Value = result  # Output below input

@xl_macro()
def macro_cast_vote():
    app = xl_app()
    dao_id = app.Range("D10").Value
    title = app.Range("E10").Value
    member = app.Range("E14").Value
    vote = app.Range("E15").Value
    result = excel_cast_vote(dao_id, title, member, vote)
    app.Range("E16").Value = result  # Output below input

@xl_macro()
def macro_check_proposal_result():
    app = xl_app()
    dao_id = app.Range("D10").Value
    title = app.Range("E10").Value
    result = excel_check_proposal_result(dao_id, title)
    app.Range("E17").Value = result  # Output below input

@xl_macro()
def macro_token_sale():
    app = xl_app()
    dao_id = app.Range("D20").Value
    buyer = app.Range("E20").Value
    amount = int(app.Range("E21").Value)
    token_price = float(app.Range("E22").Value)
    result = excel_token_sale(dao_id, buyer, amount, token_price)
    app.Range("E23").Value = result  # Output below input

@xl_macro()
def macro_treasury_contribution():
    app = xl_app()
    dao_id = app.Range("D20").Value
    contributor = app.Range("E24").Value
    amount = int(app.Range("E25").Value)
    result = excel_treasury_contribution(dao_id, contributor, amount)
    app.Range("E26").Value = result  # Output below input

@xl_macro()
def macro_fund_distribution():
    app = xl_app()
    dao_id = app.Range("D20").Value
    recipient = app.Range("E27").Value
    amount = int(app.Range("E28").Value)
    reason = app.Range("E29").Value
    result = excel_fund_distribution(dao_id, recipient, amount, reason)
    app.Range("E30").Value = result  # Output below input

@xl_macro()
def macro_investment():
    app = xl_app()
    dao_id = app.Range("D20").Value
    target_project = app.Range("E31").Value
    amount = int(app.Range("E32").Value)
    result = excel_investment(dao_id, target_project, amount)
    app.Range("E33").Value = result  # Output below input

@xl_macro()
def macro_get_blockchain_info():
    app = xl_app()
    dao_id = app.Range("D20").Value
    result = excel_get_blockchain_info(dao_id)
    app.Range("E34").Value = result  # Output below