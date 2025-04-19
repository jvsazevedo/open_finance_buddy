from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from utils.tools import tools
from utils.schemas import State

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

system_prompt = SystemMessage(content="""
You are a financial assistant.
Your goal is to help the user to understand their financial situation and to make decisions about their money.
You should use the tools provided to get the information you need.
Answer the user's question in the same language they are asking, to achieve this, you should try to identify the language they are using based on the context.
If the user provides to you his name, use it to personalize the answer.
Here is the user's name: {user_name}
If not provided, use another way to talk to the user.""")

# llm = ChatOpenAI(
#     model='gpt-4.1-mini', 
#     temperature=0.3,
#     timeout=None,
#     max_retries=3,
#     api_key=openai_api_key,  
# )

llm = ChatOllama(
    model="qwen2.5:14b",
    temperature=0.3,
)

def agent_node(state: State):
    """Agent node in the workflow graph."""
    from langgraph.prebuilt import create_react_agent
    finance_agent_graph = create_react_agent(
        model=llm,
        tools=tools,
        prompt=system_prompt,
    )
    result = finance_agent_graph.invoke(state)
    agent_response = result['messages'][-1]

    return {
        "messages": add_messages(state["messages"], [agent_response]),
    }

# Define the graph state schema
# This is the root state of the graph
# New graphs (agents) can be implemented by creating a new node
workflow = StateGraph(State)
workflow.add_node("agent", agent_node)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)

# Compile the workflow
finance_agent = workflow.compile()