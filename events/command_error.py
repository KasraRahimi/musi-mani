import traceback
from datetime import datetime
from os import makedirs

from interactions import Listener
from interactions.api.events import CommandError
from interactions.client.errors import CommandCheckFailure

EVENT_NAME = "command_error"

LOGS_DIRECTORY = "../logs/"

async def callback(event: CommandError):
    if isinstance(event.error, CommandCheckFailure):
        await event.ctx.send("You do not have the permissions to use this command", ephemeral=True)
        return
    now = datetime.now()
    today = now.date().isoformat()
    makedirs(LOGS_DIRECTORY, exist_ok=True)
    with open(f"../logs/{today}-logs.txt", "a") as file:
        time = now.strftime("%H:%M:%S")
        file.write(f"=== {time} ===\n")
        traceback.print_exception(event.error, file=file)
        file.write("\n")
    await event.ctx.send("Something went wrong", ephemeral=True)

command_error = Listener(event=EVENT_NAME, func=callback, disable_default_listeners=True)

if __name__ == "__main__":
    now = datetime.now()
    today = now.date()
    print(f'{today.isoformat()}-logs.txt')