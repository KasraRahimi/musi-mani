from interactions import slash_command, SlashContext
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet, INSUFFICIENT_FUNDS_MSG


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="horse-race",
    sub_cmd_description="Place a bet on a horse race. Let's hope your horse wins the race!",
    options=[BET_OPTION]
)
async def horse_race(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=False):
        await ctx.send(INSUFFICIENT_FUNDS_MSG)
    await ctx.send("If the command were working, you'd have enough to place a bet")
