import os 
from dotenv import load_dotenv
from interactions import Client, Intents

async def main():
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    bot = Client(token=TOKEN, intents=Intents.DEFAULT)
    
    await bot.sync_scope(cmd_scope=None, delete_cmds=True, local_cmds_json={})

    print("Bot commands have been cleared")

if __name__ == "__main__":
    main()