import traceback

from interactions import Listener
from interactions.api.events import CommandError
from interactions.client.errors import CommandCheckFailure

EVENT_NAME = "command_error"

async def callback(event: CommandError):
    if isinstance(event.error, CommandCheckFailure):
        await event.ctx.send("You do not have the permissions to use this command", ephemeral=True)
        return
    print(traceback.print_exception(event.error))
    await event.ctx.send("Something went wrong", ephemeral=True)

command_error = Listener(event=EVENT_NAME, func=callback, disable_default_listeners=True)