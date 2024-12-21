from dotenv import load_dotenv
from os import getenv
from pathlib import Path

load_dotenv()

TOKEN = getenv("TOKEN")
MONGO_DB_URI = getenv("MONGO_DB_URI")
DB_USERNAME = getenv("DB_USERNAME")
DB_PASSWORD = getenv("DB_PASSWORD")
DB_NAME = getenv("DB_NAME")

ROOT_DIRECTORY = Path(__file__).parent.resolve()

MAIN_LOGGER = "bot_logger"
