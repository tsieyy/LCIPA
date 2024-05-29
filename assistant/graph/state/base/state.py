# Top-level graph state
import operator
from typing import TypedDict, Annotated, List

from langchain_core.messages import BaseMessage


class State(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next: str
