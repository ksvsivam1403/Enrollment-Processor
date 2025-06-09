# Insurance Failed Transaction Handler

This project automates the handling of failed transactions in an insurance company using a multi-agent setup, the Model Context Protocol (MCP), CrewAI, and OpenAI integration.

## Project Structure

```
insurance-failed-tx-handler
├── data
│   └── sample_failed_transactions.csv
├── servers
│   └── insurance_mcp_server.py
├── src
│   ├── agents.py
│   ├── crew_setup.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Description

The project is designed to efficiently process and resolve failed transactions by leveraging multiple agents that communicate through an MCP server. Each agent has specific responsibilities, including data retrieval, error analysis, and suggesting resolutions.

### Components

- **Data**: Contains a sample dataset of failed transactions, structured with relevant fields such as transaction ID, user ID, error code, and timestamp.
  
- **MCP Server**: Implements the Model Context Protocol to define tools for handling failed transactions, such as retrieving transaction details, analyzing errors, and suggesting resolutions.

- **Agents**: Multiple agent classes that interact with each other to process failed transactions. Each agent has specific roles and responsibilities.

- **Crew Setup**: Initializes the CrewAI environment, setting up agents and defining the tasks they will perform.

- **Main Application**: The entry point for the application that loads the dataset, starts the MCP server, and initiates the crew setup.

## Setup Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd insurance-failed-tx-handler
   ```

2. Install the required libraries:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python src/main.py
   ```

## Usage

After running the application, the system will automatically process the sample dataset of failed transactions. The agents will work together to analyze the errors and suggest resolutions based on the defined protocols.

## Agents and Their Roles

- **Data Retrieval Agent**: Responsible for fetching transaction details from the dataset.
- **Error Analysis Agent**: Analyzes the error codes and identifies patterns or common issues.
- **Resolution Suggestion Agent**: Suggests possible resolutions based on the analysis performed by the Error Analysis Agent.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.