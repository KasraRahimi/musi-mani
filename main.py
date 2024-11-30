from commands import *
from constants import TOKEN
from interactions import Client, Intents, listen

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    @listen()
    async def on_ready():
        print("Bot is ready")
    
    bot.start()
    