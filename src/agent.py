import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph, END
from langgraph.prebuilt import ToolNode
from composio import Composio
from composio_langgraph import LanggraphProvider
from langchain_core.messages import AIMessage

load_dotenv()

# Initialize Composio
composio = Composio(
    api_key=os.getenv("COMPOSIO_API_KEY"),
    provider=LanggraphProvider()
)

USER_ID = "default_user"

# Get Google Sheets tools (read-only)
googlesheets_tools = composio.tools.get(user_id=USER_ID, toolkits=["googlesheets"])
read_only_tools = [t for t in googlesheets_tools if "GET" in t.name or "BATCH_GET" in t.name]
print(f"✅ Found {len(read_only_tools)} read-only Google Sheets tools")

# Get Gmail tools
gmail_tools = composio.tools.get(user_id=USER_ID, toolkits=["gmail"])

# Find email sending tool (prefer send over draft)
email_tool = None
for tool in gmail_tools:
    tool_name = tool.name.upper()
    if "SEND" in tool_name and "EMAIL" in tool_name and "DRAFT" not in tool_name:
        email_tool = tool
        break
    elif "POST" in tool_name and "MESSAGE" in tool_name:
        email_tool = tool
        break

# Use found tool or all Gmail tools as fallback
email_tools = [email_tool] if email_tool else gmail_tools
print(f"✅ Using Gmail tools: {email_tool.name if email_tool else 'all available'}\n")

# Combine tools
tools = read_only_tools + email_tools

# Initialize LLM and bind tools
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
llm_with_tools = llm.bind_tools(tools)
tool_node = ToolNode(tools)

# Agent node
max_iterations = 10
iteration_count = 0

def agent(state: MessagesState):
    global iteration_count
    iteration_count += 1
    
    if iteration_count > max_iterations:
        return {"messages": [AIMessage(content="Max iterations reached.")]}
    
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Routing logic
def should_continue(state: MessagesState):
    last_message = state["messages"][-1]
    
    if isinstance(last_message, AIMessage) and "Max iterations" in str(last_message.content):
        return END
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return "tools"
    
    return END

# Build graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", agent)
workflow.add_node("tools", tool_node)
workflow.set_entry_point("agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

app = workflow.compile()
print("✅ Agent ready\n")