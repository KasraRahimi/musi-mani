from interactions import slash_command, SlashContext

from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name='last_call',
    sub_cmd_description='place a bet on a game where you have to cash out before you crash',
    options=[BET_OPTION]
)
async def last_call(ctx: SlashContext, bet: int):
    await ctx.send("command not yet implemented", ephemeral=True)