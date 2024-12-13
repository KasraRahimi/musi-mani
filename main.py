import commands
import events
import logging
from pathlib import Path
from logging import handlers
from constants import TOKEN, ROOT_DIRECTORY, MAIN_LOGGER
from interactions import Client, Intents, SlashCommand, Listener

def setup_logging() -> None:
    Path(f"{ROOT_DIRECTORY}/logs").mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger(MAIN_LOGGER)
    time_handler = handlers.TimedRotatingFileHandler(f"{ROOT_DIRECTORY}/logs/bot_logs.log", when="M")
    logger.addHandler(time_handler)

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
    setup_logging()

    register_commands(bot)
    register_events(bot)

    bot.start()
    