from enum import StrEnum
from interactions import slash_command, SlashContext, ActionRow, Button, ButtonStyle, Message, Embed, EmbedAuthor, \
    EmbedField
from games.horse_race import HorseRace
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet, INSUFFICIENT_FUNDS_MSG

GAME_NAME = "Horse Race"

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

def get_horse_info_embed(ctx: SlashContext, horse_race_game: HorseRace) -> Embed:
    author = EmbedAuthor(
        name=ctx.author.display_name,
        icon_url=ctx.author.avatar_url
    )
    embed_fields = []
    for i, horse_info in enumerate(horse_race_game.horse_infos):
        embed_field = EmbedField(
            name=f"Horse {i+1}",
            value=f"Odds of winning: **{horse_info.win_odds * 100:.2f}%**\n"\
                f"Payout multiplier: **{horse_info.win_multiplier:.2f}x**",
            inline=False
        )
        embed_fields.append(embed_field)
    description = "Pick which horse you think will win."\
            "The less likely that the horse you pick wins, the larger the payout if they do win."
    return Embed(
        author=author,
        title=f"{GAME_NAME}",
        description=description,
        fields=embed_fields,
    )


async def get_initial_message(ctx: SlashContext, horse_race_game: HorseRace) -> Message:
    return await ctx.send(
        f"<@{ctx.author.id}>",
        embed=get_horse_info_embed(ctx, horse_race_game),
        components=ACTION_ROW
    )


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
    horse_race_game = HorseRace(bet=bet)
    await get_initial_message(ctx, horse_race_game)
