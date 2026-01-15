"""
Helper script to check Composio connection status and account emails.
This helps you identify which Google account email to share your Google Sheet with.
"""
import os
from dotenv import load_dotenv
from composio import Composio

load_dotenv()

# Initialize Composio
composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

USER_ID = "default_user"
GOOGLE_SHEETS_CONNECTION_ID = os.getenv("GOOGLE_SHEETS_CONNECTION_ID")
GOOGLE_MAIL_CONNECTION_ID = os.getenv("GOOGLE_MAIL_CONNECTION_ID")

print("=" * 60)
print("🔍 Checking Composio Connections")
print("=" * 60)

# Check Google Sheets connection
print("\n📊 Google Sheets Connection:")
if GOOGLE_SHEETS_CONNECTION_ID:
    try:
        connection = composio.connected_accounts.get(GOOGLE_SHEETS_CONNECTION_ID)
        print(f"   Connection ID: {GOOGLE_SHEETS_CONNECTION_ID}")
        print(f"   Status: {getattr(connection, 'status', 'Unknown')}")
        
        # Try to get account email
        account_email = None
        if hasattr(connection, 'account_email'):
            account_email = connection.account_email
        elif hasattr(connection, 'email'):
            account_email = connection.email
        elif hasattr(connection, 'user_email'):
            account_email = connection.user_email
        
        if account_email:
            print(f"   📧 Account Email: {account_email}")
            print(f"\n   ✅ IMPORTANT: Share your Google Sheet with this email!")
            print(f"      Go to your Google Sheet → Share → Add: {account_email}")
            print(f"      Give at least 'Viewer' permission for read-only access")
        else:
            print(f"   ⚠️  Could not retrieve account email from connection object")
            print(f"   Connection object attributes: {dir(connection)}")
            
            # Try to print connection details
            try:
                print(f"   Connection details: {connection}")
            except:
                pass
    except Exception as e:
        print(f"   ❌ Error getting connection: {e}")
else:
    print("   ⚠️  No GOOGLE_SHEETS_CONNECTION_ID found in .env file")
    print("   Listing all connections for user...")
    try:
        connections = composio.connected_accounts.list(user_id=USER_ID)
        if connections:
            print(f"   Found {len(connections)} connection(s):")
            for conn in connections:
                print(f"      - {conn.id} (Status: {getattr(conn, 'status', 'Unknown')})")
        else:
            print("   No connections found. Run src/main.py to authenticate.")
    except Exception as e:
        print(f"   Error listing connections: {e}")

# Check Gmail connection
print("\n📧 Gmail Connection:")
if GOOGLE_MAIL_CONNECTION_ID:
    try:
        connection = composio.connected_accounts.get(GOOGLE_MAIL_CONNECTION_ID)
        print(f"   Connection ID: {GOOGLE_MAIL_CONNECTION_ID}")
        print(f"   Status: {getattr(connection, 'status', 'Unknown')}")
        
        # Try to get account email
        account_email = None
        if hasattr(connection, 'account_email'):
            account_email = connection.account_email
        elif hasattr(connection, 'email'):
            account_email = connection.email
        elif hasattr(connection, 'user_email'):
            account_email = connection.user_email
        
        if account_email:
            print(f"   📧 Account Email: {account_email}")
    except Exception as e:
        print(f"   ❌ Error getting connection: {e}")
else:
    print("   ⚠️  No GOOGLE_MAIL_CONNECTION_ID found in .env file")

print("\n" + "=" * 60)
print("💡 Tips:")
print("   1. Make sure your Google Sheet is shared with the account email above")
print("   2. The account needs at least 'Viewer' permission")
print("   3. If you don't see the account email, check your Composio dashboard")
print("=" * 60)
