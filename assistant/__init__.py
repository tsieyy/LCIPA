
from dotenv import load_dotenv

if not load_dotenv("config/.env"):
    raise Exception("Failed to load the .env file")