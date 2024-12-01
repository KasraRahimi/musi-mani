import commands
import events
from constants import TOKEN
from interactions import Client, Intents, listen, SlashCommand, Listener


def register_commands(bot: Client):
    for command_name in commands.__all__:
        print("Loading {} command".format(command_name))
        command: SlashCommand = getattr(commands, command_name)
        bot.add_interaction(command)

def register_events(bot: Client):
    for event_name in events.__all__:
        print("Loading {} event".format(event_name))
        event: Listener = getattr(events, event_name)
        bot.add_listener(event)

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    register_commands(bot)
    register_events(bot)

    bot.start()
    