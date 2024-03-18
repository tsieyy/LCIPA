
from dotenv import load_dotenv
from pathlib import Path

if not load_dotenv((Path(__file__).parent.parent / "config/.env").absolute()):
    raise Exception("Failed to load the .env file")