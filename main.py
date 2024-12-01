import commands
import events
from constants import TOKEN
from interactions import Client, Intents, SlashCommand, Listener


def register_commands(bot: Client):
    print("== Registering commands ==")
    for command_name in commands.__all__:
        print("Loading {} command".format(command_name))
        command: SlashCommand = getattr(commands, command_name)
        bot.add_interaction(command)
    print("~~ Loaded {} (/) commands ~~\n".format(len(commands.__all__)))

def register_events(bot: Client):
    print("== Registering events ==")
    for event_name in events.__all__:
        print("Loading {} event".format(event_name))
        event: Listener = getattr(events, event_name)
        bot.add_listener(event)
    print("~~ Loaded {} events ~~\n".format(len(events.__all__)))

if __name__ == "__main__":
    bot = Client(token=TOKEN, intents=Intents.DEFAULT)

    register_commands(bot)
    register_events(bot)

    bot.start()
    