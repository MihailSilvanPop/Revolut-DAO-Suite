from pyxll import xl_func
from Backend.Features.proposals import Proposal, start_voting, cast_vote, check_voting_result
from Frontend.Input.excel_creation import daos  # Use the global DAOs dict

# Store proposals by session or DAO
excel_proposals = {}

@xl_func("string dao_id, string title, string description, string proposer: string")
def excel_create_proposal(dao_id, title, description, proposer):
    """
    Creates a proposal for the specified DAO.

    Args:
        dao_id (str): The DAO ID.
        title (str): The title of the proposal.
        description (str): The description of the proposal.
        proposer (str): The proposer of the proposal.

    Returns:
        str: Confirmation message or error message.
    """
    dao = daos.get(dao_id)
    if not dao:
        return "DAO not found."
    proposal = Proposal(title, description, proposer, dao)
    key = f"{dao_id}:{title}"
    excel_proposals[key] = proposal
    start_voting(proposal)  # Activate voting
    return f"Proposal '{title}' created."

@xl_func("string dao_id, string title, string member, string vote: string")
def excel_cast_vote(dao_id, title, member, vote):
    """
    Casts a vote on a proposal.

    Args:
        dao_id (str): The DAO ID.
        title (str): The title of the proposal.
        member (str): The member casting the vote.
        vote (str): The vote ("yes" or "no").

    Returns:
        str: Confirmation message or error message.
    """
    key = f"{dao_id}:{title}"
    proposal = excel_proposals.get(key)
    if not proposal:
        return "Proposal not found."
    return cast_vote(proposal, member, vote)

@xl_func("string dao_id, string title: string")
def excel_check_proposal_result(dao_id, title):
    """
    Checks the result of a proposal.

    Args:
        dao_id (str): The DAO ID.
        title (str): The title of the proposal.

    Returns:
        str: The result of the proposal or an error message.
    """
    dao = daos.get(dao_id)
    key = f"{dao_id}:{title}"
    proposal = excel_proposals.get(key)
    if not proposal:
        return "Proposal not found."
    return check_voting_result(proposal, dao)