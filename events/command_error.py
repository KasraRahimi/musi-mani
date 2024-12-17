from datetime import datetime
import logging
from interactions import Listener
from interactions.api.events import CommandError
from interactions.client.errors import CommandCheckFailure

from constants import MAIN_LOGGER

EVENT_NAME = "command_error"


async def callback(event: CommandError):
    if isinstance(event.error, CommandCheckFailure):
        await event.ctx.send(
            "You do not have the permissions to use this command", ephemeral=True
        )
        return
    logger = logging.getLogger(MAIN_LOGGER)
    logger.error(
        "An error occurred while executing a command:", exc_info=True, stack_info=True
    )
    await event.ctx.send("Something went wrong", ephemeral=True)


command_error = Listener(
    event=EVENT_NAME, func=callback, disable_default_listeners=True
)

if __name__ == "__main__":
    now = datetime.now()
    today = now.date()
    print(f"{today.isoformat()}-logs.txt")
