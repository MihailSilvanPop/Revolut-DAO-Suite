import uuid
import hashlib
import time
from Backend.Database import Blockchain

# --- Utility Functions ---
def generate_smart_contract_from_summary(summary):
    """
    Generates a Solidity-like smart contract based on the DAO summary.

    Args:
        summary (dict): The DAO summary.

    Returns:
        str: The generated smart contract code.
    """
    contract = f"""
    // DAO Smart Contract for {summary['name']}
    // DAO ID: {summary['dao_id']}
    // Founders: {', '.join(summary['founders'])}
    // Token: {summary['token_name']}
    // Initial Supply: {summary['initial_supply']}
    // Governance Rules: {summary['governance_rules']}
    // Members: {', '.join(summary['members'])}
    // Proposals: {len(summary['proposals'])}
    """
    return contract

def compile_solidity_to_bytecode(solidity_code):
    """
    Simulates the compilation of Solidity code to bytecode.

    Args:
        solidity_code (str): The Solidity code.

    Returns:
        str: The compiled bytecode.
    """
    return hashlib.sha256(solidity_code.encode()).hexdigest()

# --- DAO Creation Class ---
class DAOCreation:
    """
    Represents a Decentralized Autonomous Organization (DAO) with governance rules and member management.
    """

    def __init__(self, name, founders, token_name="REVO", initial_supply=1000000):
        """
        Initializes a DAO with the given parameters.

        Args:
            name (str): The name of the DAO.
            founders (list): List of founder usernames.
            token_name (str): The name of the DAO's token.
            initial_supply (int): The initial supply of the token.
        """
        self.dao_id = str(uuid.uuid4())
        self.name = name
        self.founders = founders
        self.token_name = token_name
        self.initial_supply = initial_supply
        self.creation_time = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        self.wallets = {founder: initial_supply // len(founders) for founder in founders}
        self.governance_rules = {}
        self.proposals = []
        self.members = set(founders)
        self.blockchain = Blockchain()  # Each DAO gets its own blockchain
        self._add_smart_contract_block("DAO initialized")

    def set_governance_rule(self, rule_name, value):
        """
        Sets a governance rule for the DAO.

        Args:
            rule_name (str): The name of the rule.
            value: The value of the rule.

        Returns:
            str: Confirmation message.
        """
        self.governance_rules[rule_name] = value
        self._add_smart_contract_block(f"Set governance rule: {rule_name} = {value}")
        return f"Rule '{rule_name}' set to {value}"

    def add_member(self, member_name):
        """
        Adds a new member to the DAO.

        Args:
            member_name (str): The name of the new member.

        Returns:
            str: Confirmation message.
        """
        self.members.add(member_name)
        self.wallets[member_name] = 0
        self._add_smart_contract_block(f"Added member: {member_name}")
        return f"Member '{member_name}' added."

    def create_proposal(self, title, description, proposer):
        """
        Creates a new proposal for the DAO.

        Args:
            title (str): The title of the proposal.
            description (str): The description of the proposal.
            proposer (str): The proposer of the proposal.

        Returns:
            str: The ID of the created proposal.
        """
        proposal_id = str(uuid.uuid4())
        proposal = {
            "id": proposal_id,
            "title": title,
            "description": description,
            "proposer": proposer,
            "votes": {},
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.proposals.append(proposal)
        self._add_smart_contract_block(f"Created proposal: {title}")
        return proposal_id

    def vote_on_proposal(self, proposal_id, member, vote):
        """
        Casts a vote on a proposal.

        Args:
            proposal_id (str): The ID of the proposal.
            member (str): The member casting the vote.
            vote (str): The vote ("yes" or "no").

        Returns:
            str: Confirmation message or error message.
        """
        for proposal in self.proposals:
            if proposal["id"] == proposal_id:
                proposal["votes"][member] = vote
                self._add_smart_contract_block(f"{member} voted '{vote}' on proposal '{proposal_id}'")
                return f"{member} voted '{vote}' on proposal '{proposal_id}'"
        return "Proposal not found."

    def get_summary(self):
        """
        Retrieves a summary of the DAO.

        Returns:
            dict: The DAO summary.
        """
        return {
            "dao_id": self.dao_id,
            "name": self.name,
            "founders": self.founders,
            "token_name": self.token_name,
            "initial_supply": self.initial_supply,
            "creation_time": self.creation_time,
            "members": list(self.members),
            "governance_rules": self.governance_rules,
            "proposals": self.proposals,
            "blockchain_length": len(self.blockchain.chain)
        }

    def _add_smart_contract_block(self, action_desc):
        """
        Adds a smart contract block to the DAO's blockchain.

        Args:
            action_desc (str): A description of the action.
        """
        summary = self.get_summary()
        contract = generate_smart_contract_from_summary(summary)
        bytecode = compile_solidity_to_bytecode(contract)
        tx = {
            "type": "smart_contract",
            "action": action_desc,
            "dao_name": summary["name"],
            "solidity": contract,
            "bytecode": bytecode,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        self.blockchain.add_block([tx])