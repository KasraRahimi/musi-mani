from asyncio import sleep

from interactions import slash_command, SlashContext, Button, ButtonStyle, listen, Message
from interactions.api.events import Component

from games.last_call import Outcome
from games.last_call.last_call import LastCall
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION


BUTTON_ID = 'cash_out'
CRASH_ODDS = 1 / 7

def cash_out_button(is_disabled: bool=False):
    return Button(
        custom_id=BUTTON_ID,
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
    return await ctx.send(get_in_game_message_content(ctx, last_call_game), components=cash_out_button())

async def edit_game_message(ctx: SlashContext, msg: Message, last_call_game: LastCall) -> None:
    await ctx.edit(msg, content=get_in_game_message_content(ctx, last_call_game), components=cash_out_button())

async def edit_to_win_message(ctx: SlashContext, msg: Message, last_call_game: LastCall) -> None:
    content = (
        "### Last Call",
        f"<@{ctx.author.id}>'s game",
        "",
        "😎",
        f"You just cashed out and won **{last_call_game.winnings}** talan!!"
    )
    content = "\n".join(content)
    await ctx.edit(msg, content=content, components=cash_out_button(True))

async def edit_to_lose_message(ctx: SlashContext, msg: Message) -> None:
    content = (
        "### Last Call",
        f"<@{ctx.author.id}>'s game",
        "",
        "💥",
        f"You just crashed and lost your bet."
    )
    content = "\n".join(content)
    await ctx.edit(msg, content=content, components=cash_out_button(True))

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name='last-call',
    sub_cmd_description='place a bet on a game where you have to cash out before you crash',
    options=[BET_OPTION]
)
async def last_call(ctx: SlashContext, bet: int):
    last_call_game = LastCall(bet, CRASH_ODDS)
    msg = await get_initial_message(ctx, last_call_game)

    # listen to the component for the game
    @listen(Component)
    async def on_component(event: Component):
        is_same_message = event.ctx.message.id == msg.id
        is_same_user = event.ctx.author.id == ctx.author.id

        if not is_same_user or not is_same_message:
            await event.ctx.edit_origin()
            return

        last_call_game.cash_out()
        await event.ctx.edit_origin()
    ctx.bot.add_listener(on_component)
    # == listener added to bot ==

    while last_call_game.outcome is None:
        last_call_game.step()
        await edit_game_message(ctx, msg, last_call_game)
        await sleep(1.0)

    match last_call_game.outcome:
        case Outcome.CRASH:
            await edit_to_lose_message(ctx, msg)
        case Outcome.CASH_OUT:
            await edit_to_win_message(ctx, msg, last_call_game)
