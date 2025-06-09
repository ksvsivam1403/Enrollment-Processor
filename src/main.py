from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import os
from crew_setup import setup_crew
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters
import sys
import csv

def load_data(file_path):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        raise FileNotFoundError(f"The file {file_path} does not exist.")

if __name__ == "__main__":
    os.makedirs("output", exist_ok=True)
    # Load the sample dataset of failed transactions
    data_file = os.path.join("data", "sample_failed_transactions.csv")
    failed_transactions = load_data(data_file)
    transactions = failed_transactions.to_dict(orient="records")

    server_params = StdioServerParameters(
        command=sys.executable,
        args=[os.path.join("servers", "insurance_mcp_server.py")],
        env={**os.environ},
    )
    results = []
    with MCPServerAdapter(server_params) as tools:
        for txn in transactions:
            txn_id = txn.get("transaction_id")
            if not txn_id:
                results.append({"transaction_id": None, "result": "No transaction_id provided."})
                continue
            crew = setup_crew(tools)
            # Each run processes one transaction
            result = crew.kickoff(inputs={"transaction_id": str(txn_id)})
            results.append({"transaction_id": txn_id, "result": str(result)})
    # Write all results to CSV
    output_csv = "output/crew_results.csv"
    with open(output_csv, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["transaction_id", "result"])
        writer.writeheader()
        writer.writerows(results)
    print("\nResults written to output/crew_results.csv")