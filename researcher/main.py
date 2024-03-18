
from dotenv import load_dotenv
from agents import ChiefEditorAgent
import asyncio
import json
import os

if not load_dotenv("../config/.env"):
    raise Exception("Failed to load the .env file")


def open_task():
    with open('task.json', 'r') as f:
        task = json.load(f)

    if not task:
        raise Exception("No task provided. Please include a task.json file in the root directory.")

    return task


async def main():
    task = open_task()

    chief_editor = ChiefEditorAgent(task)
    research_report = await chief_editor.run_research_task()

    return research_report

if __name__ == "__main__":
    asyncio.run(main())
