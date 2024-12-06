from interactions import slash_command, SlashContext, Button, ButtonStyle, listen, Message
from interactions.api.events import Component
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
        "😎",
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
    msg = await ctx.send("command not yet implemented, ctx_id={}".format(ctx.id), components=cash_out_button())
    last_call_game = LastCall(bet, CRASH_ODDS)
    @listen(Component)
    async def on_component(event: Component):
        if event.ctx.message.id == msg.id:
            await event.ctx.send("hehe, you pressed me")
            await msg.edit(components=cash_out_button(True))

    ctx.bot.add_listener(on_component)
