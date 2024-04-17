from colorama import Fore, Style
from enum import Enum


class AgentColor(Enum):
    RESEARCHER = Fore.LIGHTBLUE_EX
    EDITOR = Fore.YELLOW
    WRITER = Fore.LIGHTGREEN_EX
    PUBLISHER = Fore.MAGENTA
    REVIEWER = Fore.CYAN
    REVISOR = Fore.LIGHTWHITE_EX
    MASTER = Fore.LIGHTYELLOW_EX

class StreamlitColor(Enum):
    RESEARCHER = "🔎"
    EDITOR = "📝"
    WRITER = "✏️"
    PUBLISHER = "📖"
    REVIEWER = "🤓"
    REVISOR = "🧐"
    MASTER = "😇"


def print_agent_output(output:str, agent: str="RESEARCHER"):
    # print(f"{AgentColor[agent].value}{agent}: {output}{Style.RESET_ALL}")
    print(f"{StreamlitColor[agent].value} {agent}: {output}")