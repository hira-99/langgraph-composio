import os
from dotenv import load_dotenv
from composio import Composio
from datetime import datetime, timedelta
import random

load_dotenv()

composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

# Replace with your actual values
GOOGLE_SHEETS_CONNECTION_ID = os.getenv("GOOGLE_SHEETS_CONNECTION_ID")
SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")  # Get this from your Google Sheets URL
SHEET_NAME = "Orders"  # Name of the sheet tab
USER_ID = "default_user"

def add_dummy_orders():
    """Add dummy e-commerce order data to Google Sheets"""
    
    # Generate dummy data
    orders = []
    base_date = datetime.now() - timedelta(days=30)
    
    for i in range(50):  # 50 dummy orders
        order_date = base_date + timedelta(days=random.randint(0, 30))
        order_id = f"ORD-{1000 + i}"
        customer = f"Customer {i+1}"
        product = random.choice(["Laptop", "Phone", "Tablet", "Headphones", "Mouse", "Keyboard"])
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(50, 1000), 2)
        total = round(quantity * unit_price, 2)
        
        orders.append([
            order_date.strftime("%Y-%m-%d"),
            order_id,
            customer,
            product,
            quantity,
            unit_price,
            total
        ])
    
    # Add header row
    headers = [["Date", "Order ID", "Customer", "Product", "Quantity", "Unit Price", "Total"]]
    all_data = headers + orders
    
    # Use Composio to write to Google Sheets
    # Note: You'll need to use the Google Sheets API through Composio
    # This is a simplified example - you may need to adjust based on Composio's API
    
    print(f"✅ Generated {len(orders)} dummy orders")
    print("📝 Headers:", headers[0])
    print("📊 Sample order:", orders[0])
    
    return all_data

if __name__ == "__main__":
    data = add_dummy_orders()
    print(f"\n💡 Next: Add this data to your Google Sheet manually or via Composio API")
    print(f"   Spreadsheet ID: {SPREADSHEET_ID}")
    print(f"   Sheet Name: {SHEET_NAME}")