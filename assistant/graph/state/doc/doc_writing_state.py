# Document writing team graph state
import operator
from typing_extensions import TypedDict
from typing import Annotated, List

from langchain_core.messages import BaseMessage


class DocWritingState(TypedDict):
    # This tracks the team's conversation internally
    messages: Annotated[List[BaseMessage], operator.add]
    # This provides each worker with context on the others' skill sets
    team_members: str
    # This is how the supervisor tells langgraph who to work next
    next: str
    # This tracks the shared directory state
    current_files: str
