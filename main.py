import commands
from constants import TOKEN
from interactions import Client, Intents, listen, SlashCommand

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    for command_name in commands.__all__:
        command: SlashCommand= getattr(commands, command_name)
        print(f"Adding command {command.name} with resolved name {command.resolved_name}")
        bot.add_interaction(command)

    @listen()
    async def on_ready():
        print("Bot is ready")
    
    bot.start()
    