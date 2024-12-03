from dotenv import load_dotenv
from os import getenv

load_dotenv()

TOKEN = getenv("TOKEN")
MONGO_DB_URI = getenv("MONGO_DB_URI")
