from interactions import Client, Intents, listen
from interactions.api.events import Ready

from constants import TOKEN


@listen("ready")
async def on_ready(event: Ready):
    print("All bot commands have been cleared. Stopping bot")
    await bot.stop()

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT, delete_unused_application_cmds=True)
    bot.start()
