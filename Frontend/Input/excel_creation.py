from pyxll import xl_func
from Backend.Features.dao_creation import DAOCreation

# Temporary storage for DAO creation steps (in-memory, per session)
dao_creation_steps = {}

@xl_func("string session_id, string name: string")
def excel_set_dao_name(session_id, name):
    """
    Sets the name of the DAO for the given session.

    Args:
        session_id (str): The session ID.
        name (str): The name of the DAO.

    Returns:
        str: Confirmation message.
    """
    dao_creation_steps[session_id] = {"name": name}
    return f"DAO name set to '{name}'. Now enter number of founders."

@xl_func("string session_id, int num_founders: string")
def excel_set_num_founders(session_id, num_founders):
    """
    Sets the number of founders for the DAO.

    Args:
        session_id (str): The session ID.
        num_founders (int): Number of founders.

    Returns:
        str: Confirmation message or error message.
    """
    if session_id not in dao_creation_steps:
        return "Please set DAO name first."
    dao_creation_steps[session_id]["num_founders"] = num_founders
    dao_creation_steps[session_id]["founders"] = []
    return f"Number of founders set to {num_founders}. Now add founders one by one."

@xl_func("string session_id, string founder_username: string")
def excel_add_founder(session_id, founder_username):
    """
    Adds a founder to the DAO.

    Args:
        session_id (str): The session ID.
        founder_username (str): The username of the founder.

    Returns:
        str: Confirmation message or error message.
    """
    if session_id not in dao_creation_steps or "num_founders" not in dao_creation_steps[session_id]:
        return "Please set DAO name and number of founders first."
    founders = dao_creation_steps[session_id]["founders"]
    founders.append(founder_username)
    if len(founders) < dao_creation_steps[session_id]["num_founders"]:
        return f"Founder '{founder_username}' added. Add the next founder."
    else:
        return f"All founders added. Now set token name and initial supply."

@xl_func("string session_id, string token_name, int initial_supply: string")
def excel_set_token_and_supply(session_id, token_name, initial_supply):
    """
    Sets the token name and initial supply for the DAO.

    Args:
        session_id (str): The session ID.
        token_name (str): The name of the token.
        initial_supply (int): The initial supply of the token.

    Returns:
        str: Confirmation message or error message.
    """
    if session_id not in dao_creation_steps or len(dao_creation_steps[session_id].get("founders", [])) != dao_creation_steps[session_id].get("num_founders", 0):
        return "Please add all founders first."
    dao_creation_steps[session_id]["token_name"] = token_name
    dao_creation_steps[session_id]["initial_supply"] = initial_supply
    return f"Token '{token_name}' and initial supply {initial_supply} set. Now finalize DAO creation."

# Store DAOs in a global dictionary for session persistence
daos = {}

@xl_func("string session_id: string")
def excel_finalize_dao(session_id):
    """
    Finalizes the DAO creation process.

    Args:
        session_id (str): The session ID.

    Returns:
        str: Confirmation message or error message.
    """
    step = dao_creation_steps.get(session_id)
    if not step or "token_name" not in step or "initial_supply" not in step:
        return "Please complete all previous steps first."
    dao = DAOCreation(
        step["name"],
        step["founders"],
        step["token_name"],
        step["initial_supply"]
    )
    daos[dao.dao_id] = dao
    # Optionally clear the session
    del dao_creation_steps[session_id]
    return f"DAO created with ID: {dao.dao_id}"