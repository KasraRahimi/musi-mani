import traceback

from interactions import Listener
from interactions.api.events import CommandError

EVENT_NAME = "command_error"

async def callback(event: CommandError):
    print(traceback.print_exception(event.error))
    await event.ctx.send("Something went wrong", ephemeral=True)

command_error = Listener(event=EVENT_NAME, func=callback, disable_default_listeners=True)