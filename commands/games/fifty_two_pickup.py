from interactions import slash_command, SlashContext

from commands.games.constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION

GAME_NAME = "Fifty Two Pickup"

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="52-pickup",
    sub_cmd_description="Place a bet to play a classic game of 52 pickup",
    options=[BET_OPTION]
)
async def fifty_two_pickup(ctx: SlashContext, bet: int):
    pass