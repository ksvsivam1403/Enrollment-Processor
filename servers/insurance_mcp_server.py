from mcp.server.fastmcp import FastMCP
import pandas as pd

mcp = FastMCP("InsuranceTransactionHandler")

# Load the sample dataset
transactions_df = pd.read_csv("data/sample_failed_transactions.csv")

@mcp.tool()
def get_transaction_details(transaction_id: str) -> dict:
    """Retrieve details of a failed transaction by transaction ID."""
    transaction = transactions_df[transactions_df['transaction_id'].astype(str) == str(transaction_id)]
    if transaction.empty:
        return {"error": "Transaction not found"}
    return transaction.to_dict(orient='records')[0]

@mcp.tool()
def analyze_error(transaction_id: str) -> str:
    """Analyze the error code and missing attributes of a failed transaction."""
    transaction = transactions_df[transactions_df['transaction_id'].astype(str) == str(transaction_id)]
    if transaction.empty:
        return "Transaction not found"
    row = transaction.iloc[0]
    # Check for missing required fields
    missing = []
    required_fields = ['member_id', 'first_name', 'last_name', 'date_of_birth', 'ssn', 'address', 'policy_number', 'enrollment_date']
    for col in required_fields:
        if pd.isnull(row[col]) or str(row[col]).strip() == '':
            missing.append(col)
    error_code = row['error_code']
    if missing:
        return f"Error code {error_code}. Missing fields: {', '.join(missing)}."
    return f"Error code {error_code}. No missing fields detected."

@mcp.tool()
def suggest_resolution(transaction_id: str) -> str:
    """Suggest a resolution for a failed transaction based on the error code and missing attributes."""
    transaction = transactions_df[transactions_df['transaction_id'].astype(str) == str(transaction_id)]
    if transaction.empty:
        return "Transaction not found"
    row = transaction.iloc[0]
    missing = []
    required_fields = ['member_id', 'first_name', 'last_name', 'date_of_birth', 'ssn', 'address', 'policy_number', 'enrollment_date']
    for col in required_fields:
        if pd.isnull(row[col]) or str(row[col]).strip() == '':
            missing.append(col)
    error_code = row['error_code']
    if missing:
        return f"To resolve error code {error_code}, please provide the missing fields: {', '.join(missing)}."
    # Example: add more error_code-specific logic here
    if error_code == 'ERR001':
        return "ERR001: Please check member eligibility and provide all required demographic information."
    elif error_code == 'ERR002':
        return "ERR002: Policy number is invalid or missing. Please verify and resubmit."
    elif error_code == 'ERR003':
        return "ERR003: Address or contact information incomplete. Please update member profile."
    elif error_code == 'ERR004':
        return "ERR004: Enrollment date missing or invalid. Please provide a valid date."
    elif error_code == 'ERR005':
        return "ERR005: SSN missing or invalid. Please provide a valid SSN."
    elif error_code == 'ERR006':
        return "ERR006: Duplicate enrollment detected. Please review and remove duplicates."
    elif error_code == 'ERR007':
        return "ERR007: Invalid member ID. Please check and correct the member ID."
    return f"Suggested resolution for error code {error_code}: Contact support."

@mcp.tool()
def fix_transaction(transaction_id: str) -> str:
    """Simulate fixing a failed transaction by looking up missing/invalid data from a database and updating the record."""
    transaction = transactions_df[transactions_df['transaction_id'].astype(str) == str(transaction_id)]
    if transaction.empty:
        return f"Transaction {transaction_id} not found. Cannot fix."
    row = transaction.iloc[0].copy()
    required_fields = ['member_id', 'first_name', 'last_name', 'date_of_birth', 'ssn', 'address', 'policy_number', 'enrollment_date']
    missing = [col for col in required_fields if pd.isnull(row[col]) or str(row[col]).strip() == '']
    # Simulate a database of correct values (for demo, just hardcode some values)
    fake_db = {
        'policy_number': 'PN-FAKE-12345',
        'date_of_birth': '1980-01-01',
        'ssn': '999-99-9999',
        'address': '100 Default Ave',
        'enrollment_date': '2024-01-15',
        'member_id': '9999',
        'first_name': 'Default',
        'last_name': 'Member',
    }
    fixed = False
    for col in missing:
        row[col] = fake_db.get(col, f"FAKE_{col.upper()}")
        fixed = True
    if fixed:
        return f"Transaction {transaction_id} fixed: missing fields filled from database simulation: {', '.join(missing)}. Updated record: {row.to_dict()}"
    else:
        return f"Transaction {transaction_id} did not require fixing. All fields present."

if __name__ == "__main__":
    mcp.run(transport="stdio")