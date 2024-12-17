from interactions import Listener
from interactions.api.events import Ready

EVENT_NAME = "ready"


async def callback(event: Ready):
    print("The bot is now ready")


ready = Listener(event=EVENT_NAME, func=callback)
