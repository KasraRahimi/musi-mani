import asyncio

from interactions import slash_command, SlashContext, ActionRow, Button, ButtonStyle, Message, InteractionContext
from enum import Enum
from random import randint
from interactions.api.events import Component
from asyncio import sleep, exceptions
from commands.games.constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet, \
    INSUFFICIENT_FUNDS_MSG
from database import BotUser

BET_MULTIPLIER = 2

class Choice(Enum):
    HEADS = 'heads'
    TAILS = 'tails'

action_row = [
    ActionRow(
        Button(
            custom_id=Choice.HEADS.value,
            style=ButtonStyle.PRIMARY,
            label=Choice.HEADS.value.capitalize()
        ),
        Button(
            custom_id=Choice.TAILS.value,
            style=ButtonStyle.SECONDARY,
            label=Choice.TAILS.value.capitalize()
        )
    )
]

async def get_initial_message(ctx: SlashContext) -> Message:
    user_id = str(ctx.author.id)
    message = (
        "### Coin Toss",
        f"<@{user_id}>'s game",
        "",
        "Pick an outcome."
    )
    message = "\n".join(message)
    return await ctx.send(message, components=action_row)

async def get_player_choice(ctx: SlashContext, msg: Message) -> Choice | None:
    bot = ctx.bot
    async def same_user_check(component: Component):
        if str(component.ctx.author.id) == str(ctx.author.id):
            return True
        await component.ctx.edit_origin()
        return False
    try:
        user_component = await bot.wait_for_component(components=action_row, timeout=30, check=same_user_check)
    except exceptions.TimeoutError:
        await ctx.edit(msg, content="You took too long to respond", components=[])
        await asyncio.sleep(3)
        await ctx.delete(msg)
        return None
    else:
        await user_component.ctx.edit_origin(components=[])

    return Choice(user_component.ctx.custom_id)

def get_coin_toss_result() -> Choice:
    random_number = randint(0, 1)
    if random_number == 0:
        return Choice.HEADS
    else:
        return Choice.TAILS

def get_flipping_message(user_id: str, period_count: int) -> str:
    message = (
        "### Coin Toss",
        f"<@{user_id}>'s game",
        "",
        "flipping coin" + "." * period_count,
    )
    return "\n".join(message)

async def edit_message_during_coin_flip(ctx: SlashContext, msg: Message, delay_seconds: float=1.0) -> None:
    sleep_time = delay_seconds / 3
    for i in range(1, 4):
        await ctx.edit(msg, content=get_flipping_message(str(ctx.author.id), i), components=[])
        await sleep(sleep_time)

async def handle_end_game(ctx: SlashContext, msg: Message, player_choice: Choice, outcome: Choice, bet: int) -> None:
    is_player_won = player_choice == outcome
    if is_player_won:
        message_end = (
            "",
            "**You won!**",
            f"You've been awarded {bet * BET_MULTIPLIER}",
        )
    else:
        message_end = (
            "",
            "**You lost!**",
        )
    message = (
        "### Coin Toss",
        f"<@{str(ctx.author.id)}>'s game",
        "",
        f"You chose: {player_choice.value}",
        f"The outcome was: {outcome.value}",
        *message_end
    )
    message = "\n".join(message)

    if is_player_won:
        bot_user = BotUser(str(ctx.author.id))
        bot_user.deposit(bet * BET_MULTIPLIER)

    await ctx.edit(msg, content=message)



@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="coin-toss",
    sub_cmd_description="Play a game of coin toss, try to guess the outcome",
    options=[BET_OPTION]
)
async def coin_toss(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
        return

    msg = await get_initial_message(ctx)
    player_choice = await get_player_choice(ctx, msg)
    if player_choice is None:
        return
    await edit_message_during_coin_flip(ctx, msg)
    outcome = get_coin_toss_result()
    await handle_end_game(ctx, msg, player_choice, outcome, bet)
