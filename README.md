# langgraph-composio

This project is a **LangGraph + Composio demo** that:
- **Authenticates** Google Sheets and Gmail via Composio
- **Reads e-commerce order data** from a Google Sheet (read-only)
- **Uses an LLM agent (LangGraph)** to answer queries about the data
- **Sends results via email** using Gmail through Composio's Gmail toolkit

## Components

### `agent.py` - LangGraph Workflow Definition
Defines the core LangGraph workflow that:
- Initializes Composio with the LangGraph provider
- Fetches **read-only Google Sheets tools** (GET/BATCH_GET operations only)
- Fetches **Gmail tools** (specifically email sending tools, prioritizing send over draft)
- Verifies connection status and provides sharing instructions for Google Sheets
- Builds a `StateGraph` with an `agent` node and a `tools` node
- Routes between agent and tools with iteration limits (max 10) to prevent infinite loops
- Uses GPT-4o-mini as the LLM

**Key Features:**
- Automatically detects and uses email sending tools (prioritizes actual send tools over drafts)
- Verifies Google Sheets connection and displays account email for sharing instructions
- Filters Google Sheets tools to only read operations for safety

### `workflow.py` - Interactive Query Interface
Interactive command-line interface that:
- Accepts user queries about the Google Sheet data
- Sends detailed prompts to the LangGraph agent
- The agent reads from Google Sheets, calculates answers, and sends results via email
- Displays execution progress and final results

**Usage:**
- Run the script and type queries interactively
- Type `exit`, `quit`, or `q` to stop
- Example query: "What is the total sale amount for 2024-12-15?"

### `main.py` - Authentication Script
Handles authentication for both services:
- Checks for existing connections before creating new ones (avoids duplicate connections)
- Authenticates **Google Sheets** via Composio
- Authenticates **Gmail** via Composio
- Handles timeout scenarios gracefully
- Displays connection IDs for use in your `.env` file

**Features:**
- Reuses existing connections if available
- Provides clear instructions and error handling
- Supports timeout scenarios with helpful recovery options

### `data.py` - Test Data Generator
Generates **dummy e-commerce orders** that match the expected sheet schema:
- Date (YYYY-MM-DD format)
- Order ID
- Customer
- Product
- Quantity
- Unit Price
- Total

Useful for populating your Google Sheet with test data.

## Environment & Setup

### Required Environment Variables

Create a `.env` file in the project root with:

```bash
# Composio API Key (required)
COMPOSIO_API_KEY=your_composio_api_key_here

# Auth Config IDs (from Composio dashboard)
GOOGLE_SHEETS_AUTH_CONFIG_ID=your_google_sheets_auth_config_id
GOOGLE_MAIL_CONFIG_ID=your_gmail_auth_config_id

# Connection IDs (returned after authentication, optional - can be auto-detected)
GOOGLE_SHEETS_CONNECTION_ID=your_google_sheets_connection_id
GOOGLE_MAIL_CONNECTION_ID=your_gmail_connection_id

# Google Sheet Configuration
SPREADSHEET_ID=your_google_sheet_id

# Email Configuration
EMAIL_TO=recipient@example.com  # Where to send query results
```

### Getting Your Auth Config IDs

1. Go to [Composio Dashboard](https://app.composio.dev)
2. Navigate to **Integrations** → **Google Sheets** → Get your Auth Config ID
3. Navigate to **Integrations** → **Gmail** → Get your Auth Config ID

### Getting Your Spreadsheet ID

From your Google Sheets URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID/edit
```

## How to Run

### Step 1: Create and Populate Your Google Sheet

1. Create a Google Sheet with a tab named **`Orders`**
2. Add these columns (in order):
   - Date (format: YYYY-MM-DD)
   - Order ID
   - Customer
   - Product
   - Quantity
   - Unit Price
   - Total

3. **Optional:** Generate dummy data:
   ```bash
   python src/data.py
   ```
   Then manually copy the generated data into your Google Sheet.

### Step 2: Authenticate Integrations

Run the authentication script:

```bash
python src/main.py
```

This will:
- Check for existing connections first
- If none exist, prompt you to authenticate:
  - **Google Sheets**: Opens browser for OAuth, grants access
  - **Gmail**: Opens browser for OAuth, grants access
- Display connection IDs (save these to your `.env` file)

**Important:** After authentication, make sure your Google Sheet is shared with the authenticated Google account email (shown in the output). The account needs at least "Viewer" permission.

### Step 3: Configure Environment Variables

Update your `.env` file with:
- Connection IDs from Step 2
- Your `SPREADSHEET_ID`
- Your `EMAIL_TO` address (where results will be sent)

### Step 4: Run the Interactive Workflow

From the project root (with your virtualenv activated):

```bash
python src/workflow.py
```

**Usage:**
- Type your queries about the Google Sheet data
- Example: `What is the total sale amount for 2024-12-15?`
- The agent will:
  1. Read from Google Sheets using **read-only** tools
  2. Calculate the answer based on your query
  3. Send the result as an email to the address specified in `EMAIL_TO`
- Type `exit`, `quit`, or `q` to stop

## How It Works

### Workflow Flow

```
User Query → Agent (LLM) → [Needs Tools?] → Tools Node → Agent → [Done?] → End
```

1. **User enters query** → `workflow.py` creates a detailed prompt
2. **Agent receives prompt** → LLM decides what tools to use
3. **Tools node executes** → Calls Google Sheets API (read) or Gmail API (send email)
4. **Agent processes results** → LLM analyzes data and prepares response
5. **Final step** → Agent sends email with the answer
6. **Workflow ends** → Results displayed in terminal

### Safety Features

- **Read-only Google Sheets**: Only GET/BATCH_GET operations are allowed
- **Iteration limit**: Maximum 10 iterations to prevent infinite loops
- **Connection verification**: Checks connection status before use
- **Error handling**: Graceful handling of timeouts and connection issues

## Project Structure

```
langgraph-composio/
├── README.md              # This file
├── .env                   # Environment variables (create this)
├── src/
│   ├── agent.py          # LangGraph workflow definition
│   ├── workflow.py       # Interactive query interface
│   ├── main.py           # Authentication script
│   └── data.py           # Test data generator
└── venv310/              # Virtual environment (Python 3.10+)
```

## Dependencies

- `langgraph` - Workflow orchestration
- `langchain-openai` - LLM integration
- `composio` - Integration platform
- `composio-langgraph` - LangGraph provider for Composio
- `python-dotenv` - Environment variable management

## Notes

- Google Sheets usage is **strictly read-only**; write/update tools are intentionally filtered out
- Gmail is used as the **output channel** for results rather than modifying the source data
- The project uses Composio's **Gmail toolkit** for email sending
- Make sure your Google Sheet is shared with the authenticated account email
- The agent prioritizes actual email sending tools over draft creation tools

## Troubleshooting

### Connection Issues
- Run `python src/main.py` again - it will detect existing connections
- Check connection status in Composio dashboard
- Verify your auth config IDs are correct

### Google Sheets Access
- Ensure the sheet is shared with the authenticated Google account
- Check that the sheet name is exactly "Orders" (case-sensitive)
- Verify the spreadsheet ID is correct

### Email Not Sending
- Check that `EMAIL_TO` is set correctly in `.env`
- Verify Gmail connection is active
- Check that the agent found email sending tools (not just drafts)

### Tool Not Found Errors
- Ensure connections are authenticated and active
- Check that toolkits are enabled in Composio dashboard
- Verify connection IDs in `.env` match authenticated accounts
