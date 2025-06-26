from pyxll import xl_func
from Backend.Features.proposals import Proposal, draft_proposal_step_by_step, parse_proposal_keywords, validate_proposal, start_voting, cast_vote, check_voting_result
from Frontend.Input.excel_creation import daos  # Use the global DAOs dict

# Store proposals by session or DAO
excel_proposals = {}

@xl_func("string dao_id, string title, string description, string proposer: string")
def excel_create_proposal(dao_id, title, description, proposer):
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    proposal = Proposal(title, description, proposer, dao)
    key = f"{dao_id}:{title}"
    excel_proposals[key] = proposal
    start_voting(proposal)  # <-- Add this line to activate voting
    return f"Proposal '{title}' created for DAO {dao_id}."

@xl_func("string dao_id, string title, string member, string vote: string")
def excel_cast_vote(dao_id, title, member, vote):
    key = f"{dao_id}:{title}"
    proposal = excel_proposals.get(key)
    if not proposal:
        return "Proposal not found."
    # Do NOT call start_voting here!
    return cast_vote(proposal, member, vote)

@xl_func("string dao_id, string title: string")
def excel_check_proposal_result(dao_id, title):
    dao = daos.get(dao_id)
    key = f"{dao_id}:{title}"
    proposal = excel_proposals.get(key)
    if not proposal:
        return "Proposal not found."
    return check_voting_result(proposal, dao)