from interactions import slash_command, SlashContext, Button, ButtonStyle

from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION
from enum import Enum

class Id(Enum):
    id = "PRESS"

def get_my_button():
    return Button(
        custom_id=BUTTON_ID,
        style=ButtonStyle.PRIMARY,
        label="Press me",
        disabled=True
    )

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name='last-call',
    sub_cmd_description='place a bet on a game where you have to cash out before you crash',
    options=[BET_OPTION]
)
async def last_call(ctx: SlashContext, bet: int):
    await ctx.send("command not yet implemented, ctx_id={}".format(ctx.id), components=my_button)