from crewai import Crew, Agent, Task
from mcp import StdioServerParameters
import os
import sys

def setup_crew(tools):
    # Define agents for handling failed transactions, each with access to MCP tools
    data_retrieval_agent = Agent(
        role="DataRetriever",
        goal="Retrieve transaction details for the given transaction_id using the MCP tools.",
        backstory="An agent responsible for fetching transaction information.",
        tools=tools,
        verbose=True,
    )

    error_analysis_agent = Agent(
        role="ErrorAnalyzer",
        goal="Analyze the error code and missing attributes for the given transaction_id using the MCP tools.",
        backstory="An agent that examines error codes and missing data to determine the cause of failures.",
        tools=tools,
        verbose=True,
    )

    resolution_agent = Agent(
        role="ResolutionSuggester",
        goal="Suggest resolutions for the given transaction_id based on the analysis using the MCP tools.",
        backstory="An agent that provides solutions for the identified issues.",
        tools=tools,
        verbose=True,
    )

    fixer_agent = Agent(
        role="FixerAgent",
        goal="Fix the failed transaction for the given transaction_id by simulating a database lookup and updating missing or invalid fields using the MCP tools.",
        backstory="An agent that mimics a human operator by looking up missing data in a database and updating the record.",
        tools=tools,
        verbose=True,
    )

    # Initialize the crew with agents and tasks
    crew = Crew(
        agents=[data_retrieval_agent, error_analysis_agent, resolution_agent, fixer_agent],
        tasks=[
            Task(
                description="Retrieve transaction details for transaction ID {transaction_id} using the MCP tools.",
                expected_output="Transaction details retrieved successfully.",
                agent=data_retrieval_agent,
            ),
            Task(
                description="Analyze the error code and missing attributes for transaction ID {transaction_id} using the MCP tools.",
                expected_output="Error analysis completed.",
                agent=error_analysis_agent,
            ),
            Task(
                description="Suggest resolutions for the identified errors for transaction ID {transaction_id} using the MCP tools.",
                expected_output="Resolution suggestions provided.",
                agent=resolution_agent,
            ),
            Task(
                description="Fix the failed transaction for transaction ID {transaction_id} by simulating a database lookup and updating missing or invalid fields using the MCP tools.",
                expected_output="Transaction fixed and updated successfully, or a reason why it could not be fixed.",
                agent=fixer_agent,
            ),
        ],
        verbose=True,
    )

    return crew

if __name__ == "__main__":
    crew = setup_crew()
    crew.kickoff()