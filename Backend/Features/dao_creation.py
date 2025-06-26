import uuid
import hashlib
import time
from Backend.Database import Blockchain

# --- Place these at the top level, before the class ---
def generate_smart_contract_from_summary(summary):
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
    return hashlib.sha256(solidity_code.encode()).hexdigest()

class DAOCreation:
    def __init__(self, name, founders, token_name="REVO", initial_supply=1000000):
        self.dao_id = str(uuid.uuid4())
        self.name = name
        self.founders = founders  # List of founder names
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
        self.governance_rules[rule_name] = value
        self._add_smart_contract_block(f"Set governance rule: {rule_name} = {value}")
        return f"Rule '{rule_name}' set to {value}"

    def add_member(self, member_name):
        self.members.add(member_name)
        self.wallets[member_name] = 0
        self._add_smart_contract_block(f"Added member: {member_name}")
        return f"Member '{member_name}' added."

    def create_proposal(self, title, description, proposer):
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
        for proposal in self.proposals:
            if proposal["id"] == proposal_id:
                proposal["votes"][member] = vote
                self._add_smart_contract_block(f"{member} voted '{vote}' on proposal '{proposal_id}'")
                return f"{member} voted '{vote}' on proposal '{proposal_id}'"
        return "Proposal not found."

    def get_summary(self):
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