# The agent state is the input to each node in the graph
import operator
from typing import TypedDict, Annotated, Sequence

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str
