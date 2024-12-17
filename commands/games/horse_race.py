from enum import StrEnum

from interactions import slash_command, SlashContext, ActionRow, Button, ButtonStyle

from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet, INSUFFICIENT_FUNDS_MSG

class HorseChoice(StrEnum):
    ONE = '0'
    TWO = '1'
    THREE = '2'
    FOUR = '3'

ACTION_ROW = [ActionRow(
    Button(
        style=ButtonStyle.SECONDARY,
        emoji='1️⃣',
        custom_id=HorseChoice.ONE
    ),
    Button(
        style=ButtonStyle.SECONDARY,
        emoji='2️⃣',
        custom_id=HorseChoice.TWO
    ),
    Button(
        style=ButtonStyle.SECONDARY,
        emoji='3️⃣',
        custom_id=HorseChoice.THREE
    ),
    Button(
        style=ButtonStyle.SECONDARY,
        emoji='4️⃣',
        custom_id=HorseChoice.FOUR
    )
)]

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="horse-race",
    sub_cmd_description="Place a bet on a horse race. Let's hope your horse wins the race!",
    options=[BET_OPTION]
)
async def horse_race(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=False):
        await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
        return
    await ctx.send("If the command were working, you'd have enough to place a bet")
