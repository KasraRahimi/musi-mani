import os 
from dotenv import load_dotenv
from interactions import Client, Intents, listen
from commands import *

if __name__ == "__main__":
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    @listen()
    async def on_ready():
        print("Bot is ready")
    
    bot.start()
    