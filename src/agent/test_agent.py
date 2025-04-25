from langchain_core.messages import HumanMessage
import sys
import os

# Add the parent directory to the path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from agent.finance_manager import finance_agent


def print_stream(stream) -> str:
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


def test(x) -> str:
    return False


if __name__ == "__main__":
    while True:
        user_input = input("User: ")
        if user_input.lower() == "exit":
            break

        agent_state = {
            "messages": [],
            "user_id": "123",
            "user_name": "John Doe",
        }
        agent_state["messages"].append(HumanMessage(content=user_input))
        print_stream(finance_agent.stream(agent_state, stream_mode="values"))
