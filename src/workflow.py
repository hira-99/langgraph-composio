import os
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from agent import app

load_dotenv()

EMAIL_TO = os.getenv("EMAIL_TO")  # Recipient email address
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")


def run_query(query: str):
    prompt = f"""You are an AI assistant that can read from Google Sheets and send emails via Gmail.

Google Sheet:
- Spreadsheet ID: {SPREADSHEET_ID}
- Sheet name: "Orders"
- Columns: Date, Order ID, Customer, Product, Quantity, Unit Price, Total
- IMPORTANT: Only READ from the sheet, never write to it.

Instructions:
1. Read data from the Google Sheet to answer the question.
2. Calculate the answer.
3. Send the final answer as an email to: {EMAIL_TO}
   - Subject: "Query Result: {query[:50]}"
   - Body: Include the question and the calculated answer clearly formatted

Question: {query}
"""

    config = {"configurable": {"thread_id": "1"}}
    final_state = app.invoke({"messages": [HumanMessage(content=prompt)]}, config=config)
    
    if final_state and "messages" in final_state:
        print(f"✅ Completed with {len(final_state['messages'])} messages")
    
    return final_state


if __name__ == "__main__":
    print("=" * 60)
    print("📧 Query Google Sheets → Send via Email")
    print("=" * 60)
    print("Type 'exit' to quit.\n")

    while True:
        query = input("You: ").strip()
        if not query:
            continue
        if query.lower() in {"exit", "quit", "q"}:
            break
        
        print()
        run_query(query)
        print()
