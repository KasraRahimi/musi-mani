import commands
from constants import TOKEN
from interactions import Client, Intents, listen, SlashCommand


def register_commands(bot: Client):
    for command_name in commands.__all__:
        command: SlashCommand = getattr(commands, command_name)
        bot.add_interaction(command)

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    register_commands(bot)

    @listen()
    async def on_ready():
        print("Bot is ready")

    bot.start()
    