# Revolut DAO Suite

## Overview
The Revolut DAO Suite is a comprehensive framework for creating, managing, and interacting with Decentralized Autonomous Organizations (DAOs). It provides tools for DAO creation, proposal management, blockchain integration, and transaction handling. The suite is designed to simulate DAO operations and governance rules using Python, with support for blockchain-like functionality.

---

## Purpose of the Project
This project serves as the operational MVP for the fintech assignment, focusing on the creation and management of Decentralized Autonomous Organizations (DAOs). The Revolut DAO Suite showcases the potential of decentralized finance (DeFi) and its applications in modern financial systems, aligning with the objectives of the fintech.

---

## Setup Instructions

### Prerequisites
- **Python**: Version 3.11 or higher.
- **Docker**: Ensure Docker is installed for containerized development.
- **Poetry**: Dependency management is handled using Poetry.

### Steps to Set Up
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd Revolut-DAO-Suite
   ```

2. **Set Up the Development Environment**:
   - If using Docker:
     ```bash
     docker build -t revolut-dao-suite .
     docker run -it revolut-dao-suite
     ```
   - If using Poetry:
     ```bash
     poetry install --with tests
     poetry shell
     ```

3. **Activate the Virtual Environment**:
   ```bash
   source .venv/bin/activate
   ```

4. **Run Unit Tests**:
   ```bash
   pytest Tests/
   ```

5. **Start Development**:
   Open the project in Visual Studio Code. The [`.devcontainer`](.devcontainer ) folder contains configurations for containerized development.

---

## Architecture

### Backend
The backend is organized into two main modules:
1. **Database**:
   - [`Blockchain`](Backend/Database/blockchain.py ): Implements a basic blockchain simulation with blocks, transactions, and a genesis block.
   - [`MultiSigWallet`](Backend/Database/blockchain.py ): Provides multisig wallet functionality for transaction approvals.

2. **Features**:
   - [`Backend/Features/dao_creation.py`](Backend/Features/dao_creation.py ): Handles DAO creation, governance rules, and member management.
   - [`Backend/Features/transactions.py`](Backend/Features/transactions.py ): Implements transaction types such as token sales, treasury contributions, fund distributions, and investments.
   - [`Backend/Features/proposals.py`](Backend/Features/proposals.py ): Manages DAO proposals, voting, and results.
   - [`Backend/Features/smart_contracts.py`](Backend/Features/smart_contracts.py ): Generates Solidity-like smart contracts based on governance rules.

### Frontend
The frontend integrates with Excel using the PyXLL library. It provides functions for DAO creation, transaction execution, and proposal management:
- [`Frontend/Input/excel_creation.py`](Frontend/Input/excel_creation.py ): Facilitates DAO creation step-by-step.
- [`Frontend/Input/excel_transactions.py`](Frontend/Input/excel_transactions.py ): Handles DAO transactions via Excel functions.
- [`Frontend/Input/excel_proposals.py`](Frontend/Input/excel_proposals.py ): Manages proposals and voting through Excel.

### Unit Tests
The [`Tests`](Tests ) folder contains comprehensive unit tests for all major components:
- **Blockchain**: Tests block creation, hash uniqueness, and chain structure.
- **DAO Creation**: Validates DAO initialization, governance rules, and member addition.
- **Transactions**: Ensures proper execution and recording of transactions.
- **Proposals**: Tests proposal creation, voting, and result validation.
- **Excel Integration**: Verifies Excel-based DAO creation, transactions, and proposals.

---

## Frameworks and Libraries
- **Python**: Core programming language.
- **PyXLL**: Integrates Python functions with Excel.
- **Pandas** and **NumPy**: Used for data manipulation and numerical operations.
- **Poetry**: Dependency management.
- **Docker**: Containerized development environment.

---

## Docker Setup
The project includes a [`Dockerfile`](Dockerfile ) for containerized development:
- **Base Image**: `python:3.11-slim`.
- **Dependencies**: Installs Poetry and required system libraries.
- **Commands**:
  - `poetry install --no-root`: Installs dependencies without packaging the project.
  - `CMD ["/bin/bash"]`: Starts a shell by default.

---

## Classes and Functions

### Backend
#### [`Blockchain`](Backend/Database/blockchain.py )
- [`create_genesis_block()`](Backend/Database/blockchain.py ): Creates the initial block in the chain.
- [`add_block(transactions)`](Backend/Database/blockchain.py ): Adds a new block to the chain.

#### [`MultiSigWallet`](Backend/Database/blockchain.py )
- [`propose_transaction(transaction)`](Backend/Database/blockchain.py ): Proposes a transaction for approval.
- [`approve_transaction(transaction_index, owner)`](Backend/Database/blockchain.py ): Approves a transaction.
- [`execute_transaction(transaction_index)`](Backend/Database/blockchain.py ): Executes a transaction after sufficient approvals.

#### [`DAOCreation`](Backend/Features/dao_creation.py )
- [`set_governance_rule(rule_name, value)`](Backend/Features/dao_creation.py ): Sets governance rules for the DAO.
- [`add_member(member_name)`](Backend/Features/dao_creation.py ): Adds a new member to the DAO.
- [`create_proposal(title, description, proposer)`](Backend/Features/dao_creation.py ): Creates a new proposal.
- [`vote_on_proposal(proposal_id, member, vote)`](Backend/Features/dao_creation.py ): Casts a vote on a proposal.

#### [`Proposal`](Backend/Features/proposals.py )
- [`to_string()`](Backend/Features/proposals.py ): Converts proposal details to a string.

#### `Transactions`
- [`TokenSaleTransaction`](Backend/Features/transactions.py ): Handles token sales.
- [`TreasuryContributionTransaction`](Backend/Features/transactions.py ): Manages treasury contributions.
- [`FundDistributionTransaction`](Backend/Features/transactions.py ): Distributes funds for specific purposes.
- [`InvestmentTransaction`](Backend/Features/transactions.py ): Executes investments in projects.

#### `Smart Contracts`
- [`parse_governance_rule(input_str)`](Backend/Features/smart_contracts.py ): Parses governance rules from user input.
- [`generate_solidity_quorum(percent, plus)`](Backend/Features/smart_contracts.py ): Generates Solidity code for quorum rules.
- [`add_contract_to_blockchain(solidity_code, blockchain)`](Backend/Features/smart_contracts.py ): Adds a smart contract to the blockchain.

### Frontend
#### Excel Functions
- [`excel_set_dao_name(session_id, name)`](Frontend/Input/excel_creation.py ): Sets the DAO name.
- [`excel_set_num_founders(session_id, num_founders)`](Frontend/Input/excel_creation.py ): Specifies the number of founders.
- [`excel_add_founder(session_id, founder_username)`](Frontend/Input/excel_creation.py ): Adds a founder to the DAO.
- [`excel_finalize_dao(session_id)`](Frontend/Input/excel_creation.py ): Finalizes DAO creation.
- [`excel_set_token_and_supply(session_id, token_name, total_supply)`](Frontend/Input/excel_creation.py ): Sets the token name and total supply for the DAO.
- [`excel_token_sale(dao_id, buyer, amount, token_price)`](Frontend/Input/excel_transactions.py ): Executes a token sale.
- [`excel_treasury_contribution(dao_id, contributor, amount)`](Frontend/Input/excel_transactions.py ): Handles treasury contributions.
- [`excel_fund_distribution(dao_id, recipient, amount, reason)`](Frontend/Input/excel_transactions.py ): Distributes funds.
- [`excel_investment(dao_id, target_project, amount)`](Frontend/Input/excel_transactions.py ): Executes investments.
- [`excel_create_proposal(dao_id, title, description, proposer)`](Frontend/Input/excel_proposals.py ): Creates a proposal.
- [`excel_cast_vote(dao_id, title, member, vote)`](Frontend/Input/excel_proposals.py ): Casts a vote on a proposal.
- [`excel_check_proposal_result(dao_id, title)`](Frontend/Input/excel_proposals.py ): Checks the result of a proposal.
- [`excel_get_blockchain_info()`](Frontend/Input/excel_creation.py ): Retrieves and displays blockchain information.

---

## Testing
It is recommended to run unit tests using the Testing sidebar in Visual Studio Code for better visibility and debugging. Follow these steps:

1. Open the Testing sidebar:
   - Search for and select `View: Show Testing`.

2. Discover and run tests:
   - The Testing sidebar will automatically discover all unit tests in the `Tests` folder.
   - Click the play button next to individual tests or the "Run All Tests" button to execute all tests.

Alternatively, you can run unit tests using `pytest` from the terminal:
```bash
pytest Tests/
```


---

## License
This project is licensed under the MIT License.

