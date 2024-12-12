import datetime
from asyncio import sleep

from interactions import slash_command, SlashContext, Button, ButtonStyle, listen, Message, Snowflake, SnowflakeObject, \
    component_callback, ComponentContext
from interactions.api.events import Component

from database import BotUser
from games.last_call import Outcome
from games.last_call.last_call import LastCall
from models.game_stat import GameStat
from .blackjack import GAME_NAME
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet
from ..utils import get_button_id, ButtonIdInfo

BUTTON_ID = 'cash_out'
GAME_NAME = 'Last Call'
CRASH_ODDS = 1 / 7

def cash_out_button(ctx: SlashContext, is_disabled: bool=False):
    return Button(
        custom_id=get_button_id(BUTTON_ID, ctx),
        style=ButtonStyle.PRIMARY,
        label="Cash out",
        emoji='💰',
        disabled=is_disabled
    )

def get_in_game_message_content(ctx: SlashContext, last_call_game: LastCall) -> str:
    content = (
        "### Last Call",
        f"<@{ctx.author.id}>'s game",
        "",
        "🙂",
        f"__potential win__: {last_call_game.potential_winnings} talan"
    )
    return "\n".join(content)

async def get_initial_message(ctx: SlashContext, last_call_game: LastCall) -> Message:
    return await ctx.send(get_in_game_message_content(ctx, last_call_game), components=cash_out_button(ctx))

async def edit_game_message(ctx: SlashContext, msg: Message, last_call_game: LastCall) -> None:
    await ctx.edit(msg, content=get_in_game_message_content(ctx, last_call_game))

async def edit_to_win_message(ctx: SlashContext, msg: Message, last_call_game: LastCall) -> None:
    content = (
        "### Last Call",
        f"<@{ctx.author.id}>'s game",
        "",
        "😎",
        f"You just cashed out and won **{last_call_game.winnings}** talan!!"
    )
    content = "\n".join(content)
    await ctx.edit(msg, content=content, components=cash_out_button(ctx, True))

async def edit_to_lose_message(ctx: SlashContext, msg: Message) -> None:
    content = (
        "### Last Call",
        f"<@{ctx.author.id}>'s game",
        "",
        "💥",
        f"You just crashed and lost your bet."
    )
    content = "\n".join(content)
    await ctx.edit(msg, content=content, components=cash_out_button(ctx, True))

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name='last-call',
    sub_cmd_description='Place a bet on a game of last call. Cash out before the game crashes.',
    options=[BET_OPTION]
)
async def last_call(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send("You do not have enough talan to place this bet", ephemeral=True)
        return

    last_call_game = LastCall(bet, CRASH_ODDS)
    msg = await get_initial_message(ctx, last_call_game)

    # listen to the component for the game
    @component_callback(get_button_id(BUTTON_ID, ctx))
    async def on_component(cmp_ctx: ComponentContext):
        is_same_message = cmp_ctx.message.id == msg.id
        is_same_user = cmp_ctx.author.id == ctx.author.id
        if not is_same_user or not is_same_message:
            await cmp_ctx.edit_origin()
            return

        last_call_game.cash_out()
        await cmp_ctx.edit_origin()
    ctx.bot.add_component_callback(on_component)
    # == listener added to bot ==

    while last_call_game.outcome is None:
        last_call_game.step()
        if last_call_game.outcome is not None:
            break
        await edit_game_message(ctx, msg, last_call_game)
        await sleep(1.0)

    bot_user = BotUser(str(ctx.author.id))
    match last_call_game.outcome:
        case Outcome.CRASH:
            await edit_to_lose_message(ctx, msg)
        case Outcome.CASH_OUT:
            bot_user.deposit(last_call_game.winnings)
            await edit_to_win_message(ctx, msg, last_call_game)

    game_stat = GameStat(
        name=GAME_NAME,
        date=datetime.datetime.now(),
        bet=bet,
        payout=last_call_game.winnings,
        is_win=last_call_game.outcome == Outcome.CASH_OUT
    )
    bot_user.add_game_stat(game_stat)
