import datetime
from asyncio import exceptions
from interactions import (
    Button,
    ButtonStyle,
    ActionRow,
    ComponentContext,
    slash_command,
    SlashContext,
    Message,
)
from enum import StrEnum
from interactions.api.events import Component

from database import BotUser
from games.blackjack import Blackjack, Outcome
from models.game_stat import GameStat
from .constants import (
    COMMAND_NAME,
    COMMAND_DESCRIPTION,
    BET_OPTION,
    can_player_bet,
    INSUFFICIENT_FUNDS_MSG,
)

GAME_NAME = "Blackjack"


class Choice(StrEnum):
    HIT = "hit"
    STAND = "stand"
    DOUBLE = "double"


def get_choice_action_row(has_double=False):
    hit = Button(
        custom_id=Choice.HIT, style=ButtonStyle.PRIMARY, label="Hit", emoji="👇"
    )
    stand = Button(
        custom_id=Choice.STAND, style=ButtonStyle.SECONDARY, label="Stand", emoji="🤚"
    )
    double = Button(
        custom_id=Choice.DOUBLE,
        style=ButtonStyle.DANGER,
        label="Double",
        emoji="☝️",
        disabled=not has_double,
    )
    action_row = ActionRow(hit, stand, double)
    return [action_row]


def get_game_message_content(ctx: SlashContext, blackjack: Blackjack) -> str:
    user_mention = f"<@{str(ctx.author.id)}>"
    message = (
        "### Blackjack",
        f"{user_mention}'s game",
        "",
        f"The dealer's first card is: **{blackjack.dealer_first_card}**",
        "",
        "Your cards are:",
        *map(lambda card: f"- {card}", blackjack.player_hand),
        f"your current value is: {blackjack.player_value}",
    )
    return "\n".join(message)


async def get_initial_message(ctx: SlashContext, blackjack: Blackjack) -> Message:
    return await ctx.send(
        get_game_message_content(ctx, blackjack),
        components=get_choice_action_row(has_double=blackjack.can_double),
    )


async def update_game_message(
    ctx: SlashContext, msg: Message, blackjack: Blackjack
) -> None:
    await ctx.edit(
        msg,
        content=get_game_message_content(ctx, blackjack),
        components=get_choice_action_row(has_double=blackjack.can_double),
    )


def get_final_game_update_message(userId: str, blackjack: Blackjack) -> str:
    user_mention = f"<@{userId}>"

    status_message = ()
    match blackjack.outcome:
        case Outcome.WIN:
            status_message = ("You won!!", f"You've been awarded {blackjack.winnings}")
        case Outcome.LOSE:
            status_message = ("You lost!",)
        case Outcome.DRAW:
            status_message = (
                "It was a draw",
                f"You've been given back {blackjack.winnings}",
            )
        case Outcome.BLACKJACK:
            status_message = (
                "Woah! You got blackjack!",
                f"You've been awarded {blackjack.winnings}",
            )

    message = (
        "### Blackjack (END)",
        f"{user_mention}'s game",
        "",
        f"The dealer's cards were:",
        *map(lambda card: f"- {card}", blackjack.dealer_hand),
        f"the dealer's value was: {blackjack.dealer_value}",
        "",
        *status_message,
    )

    return "\n".join(message)


async def get_component_ctx(
    ctx: SlashContext, msg: Message, action_row
) -> None | ComponentContext:
    async def same_user_check(component: Component):
        if component.ctx.author.id == ctx.author.id:
            return True
        await component.ctx.edit_origin()
        return False

    try:
        used_component: Component = await ctx.bot.wait_for_component(
            messages=msg, components=action_row, timeout=30, check=same_user_check
        )
    except exceptions.TimeoutError as e:
        return None
    else:
        await used_component.ctx.edit_origin()
        return used_component.ctx


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="blackjack",
    sub_cmd_description="Place a bet on a regular game of blackjack.",
    options=[BET_OPTION],
)
async def blackjack(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
        return

    user_id = str(ctx.author.id)
    blackjack = Blackjack(bet)

    blackjack.start()
    message = await get_initial_message(ctx, blackjack)

    while blackjack.outcome is None:
        component_ctx = await get_component_ctx(
            ctx, message, get_choice_action_row(has_double=blackjack.can_double)
        )
        if component_ctx is None:
            await message.edit(content="You failed to reply in time", components=[])
            return

        match component_ctx.custom_id:
            case Choice.HIT:
                blackjack.hit()
            case Choice.STAND:
                blackjack.stand()
            case Choice.DOUBLE:
                if not can_player_bet(ctx, bet, do_withdraw=True):
                    await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
                    blackjack.can_double = False
                else:
                    blackjack.double()

        await update_game_message(ctx, message, blackjack)

    await ctx.edit(message, components=[])

    bot_user = BotUser(user_id)
    bot_user.deposit(blackjack.winnings)
    game_stat = GameStat(
        name=GAME_NAME,
        date=datetime.datetime.now(),
        bet=bet,
        payout=blackjack.winnings,
        is_win=blackjack.outcome == Outcome.WIN
        or blackjack.outcome == Outcome.BLACKJACK,
    )
    bot_user.add_game_stat(game_stat)

    await message.reply(get_final_game_update_message(user_id, blackjack))
