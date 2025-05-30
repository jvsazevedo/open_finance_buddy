from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_id: int
    user_name: str
