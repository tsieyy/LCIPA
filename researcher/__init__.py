from dotenv import load_dotenv
from pathlib import Path

from researcher.agents import ChiefEditorAgent
from researcher.agents.master import RESEARCHER_OUTPUT_PATH

if not load_dotenv((Path(__file__).parent.parent / "config/.env").absolute()):
    raise Exception("Failed to load the .env file")


async def run_task(task):
    chief_editor = ChiefEditorAgent(task)
    research_report = await chief_editor.run_research_task()
    return research_report
