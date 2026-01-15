import os
from dotenv import load_dotenv
from composio import Composio
from composio.exceptions import ComposioSDKTimeoutError

load_dotenv()

# Initialize Composio
composio = Composio(api_key=os.getenv("COMPOSIO_API_KEY"))

def authenticate_account(app_name, auth_config_id, user_id="default_user"):
    """Authenticate a Google Sheets or Gmail account"""
    print(f"\n🔐 Checking {app_name} connection...")
    
    # Check for existing connections
    try:
        existing_connections = composio.connected_accounts.list(
            user_id=user_id,
            auth_config_id=auth_config_id,
        )
        if existing_connections:
            connection_id = existing_connections[0].id
            print(f"✅ Using existing connection: {connection_id}\n")
            return connection_id
    except Exception:
        pass
    
    # Create new connection
    print(f"🔐 Creating new {app_name} connection...")
    connection_request = composio.connected_accounts.initiate(
        user_id=user_id,
        auth_config_id=auth_config_id,
        allow_multiple=True,
    )
    
    connection_id = connection_request.id
    print(f"📝 Connection ID: {connection_id}")
    print(f"👉 Please visit: {connection_request.redirect_url}")
    print("⏳ Waiting for authentication (5 minutes)...\n")
    
    try:
        connection_request.wait_for_connection(timeout=300)
        print(f"✅ {app_name} authenticated successfully!")
        print(f"📝 Connection ID: {connection_id}\n")
    except ComposioSDKTimeoutError:
        print(f"⏱️  Timeout. Connection ID: {connection_id}")
        print("💡 Run this script again to check if connection is active.\n")
    
    return connection_id

if __name__ == "__main__":
    GOOGLE_SHEETS_AUTH_CONFIG_ID = os.getenv("GOOGLE_SHEETS_AUTH_CONFIG_ID")
    GOOGLE_MAIL_AUTH_CONFIG_ID = os.getenv("GOOGLE_MAIL_CONFIG_ID")
    
    # Authenticate Google Sheets
    google_sheets_connection_id = authenticate_account(
        "Google Sheets", 
        GOOGLE_SHEETS_AUTH_CONFIG_ID
    )
    
    # Authenticate Gmail
    gmail_connection_id = authenticate_account(
        "Gmail", 
        GOOGLE_MAIL_AUTH_CONFIG_ID
    )
    
    print("\n🎉 All accounts authenticated!")
    print(f"Google Sheets Connection ID: {google_sheets_connection_id}")
    print(f"Gmail Connection ID: {gmail_connection_id}")
    print("\n💡 Save these connection IDs - you'll need them for the main workflow!")