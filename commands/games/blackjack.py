from asyncio import exceptions
from interactions import InteractionContext, Button, ButtonStyle, ActionRow, \
    Client, ComponentContext, slash_command, SlashContext
from enum import Enum
from interactions.api.events import Component

from database import BotUser
from games.blackjack import Blackjack, Outcome
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet, INSUFFICIENT_FUNDS_MSG


class Choice(Enum):
    HIT = 'hit'
    STAND = 'stand'
    DOUBLE = 'double'

def get_choice_action_row(has_double=False):
    hit = Button(
        custom_id=Choice.HIT.value,
        style=ButtonStyle.PRIMARY,
        label="Hit"
    )
    stand = Button(
        custom_id=Choice.STAND.value,
        style=ButtonStyle.SECONDARY,
        label="Stand"
    )
    double = Button(
        custom_id=Choice.DOUBLE.value,
        style=ButtonStyle.DANGER,
        label="Double"
    )
    if has_double:
        action_row = ActionRow(hit, stand, double)
    else:
        action_row = ActionRow(hit, stand)

    return [action_row]

def get_game_update_message(userId: str, blackjack: Blackjack) -> str:
    user_mention = f"<@{userId}>"

    message = (
        "### Blackjack",
        f"{user_mention}'s game",
        "",
        f"The dealer's first card is: **{blackjack.dealer_first_card}**",
        "",
        "Your cards are:",
        *map(lambda card: f"- {card}", blackjack.player_hand),
        f"your current value is: {blackjack.player_value}"
    )

    return "\n".join(message)

def get_final_game_update_message(userId: str, blackjack: Blackjack) -> str:
    user_mention = f"<@{userId}>"

    status_message = ()
    match blackjack.outcome:
        case Outcome.WIN:
            status_message = (
                "You won!!",
                f"You've been awarded {blackjack.winnings}"
            )
        case Outcome.LOSE:
            status_message = (
                "You lost!",
            )
        case Outcome.DRAW:
            status_message = (
                "It was a draw",
                f"You've been given back {blackjack.winnings}"
            )
        case Outcome.BLACKJACK:
            status_message = (
                "Woah! You got blackjack!",
                f"You've been awarded {blackjack.winnings}"
            )

    message = (
        "### Blackjack (END)",
        f"{user_mention}'s game",
        "",
        f"The dealer's cards were:",
        *map(lambda card: f"- {card}", blackjack.dealer_hand),
        f"the dealer's value was: {blackjack.dealer_value}",
        "",
        *status_message
    )

    return "\n".join(message)

async def get_component_ctx(bot: Client, action_row, user_id: str) -> None | ComponentContext:
    async def same_user_check(component: Component):
        if str(component.ctx.author.id) == user_id:
            return True
        await component.ctx.edit_origin()
        return False

    try:
        used_component: Component = await bot.wait_for_component(
            components=action_row,
            timeout=30,
            check=same_user_check
        )
    except exceptions.TimeoutError as e:
        return None
    else:
        return used_component.ctx


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="blackjack",
    sub_cmd_description="Play a game of blackhack",
    options=[BET_OPTION]
)
async def blackjack(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
        return

    bot: Client = ctx.bot
    user_id = str(ctx.author.id)
    blackjack = Blackjack(bet)

    blackjack.start()
    message = await ctx.send(
        get_game_update_message(user_id, blackjack),
        components=get_choice_action_row(has_double=blackjack.can_double)
    )

    while blackjack.outcome is None:
        component_ctx = await get_component_ctx(bot, get_choice_action_row(has_double=blackjack.can_double), user_id)
        if component_ctx is None:
            await message.edit(content="You failed to reply in time", components=[])
            return

        match component_ctx.custom_id:
            case Choice.HIT.value:
                blackjack.hit()
            case Choice.STAND.value:
                blackjack.stand()
            case Choice.DOUBLE.value:
                if not can_player_bet(ctx, bet, do_withdraw=True):
                    await ctx.send(INSUFFICIENT_FUNDS_MSG, ephemeral=True)
                    blackjack.can_double = False
                else:
                    blackjack.double()


        await component_ctx.edit_origin(content=get_game_update_message(user_id, blackjack), components=get_choice_action_row(has_double=blackjack.can_double))

    await ctx.edit(message, components=[])

    bot_user = BotUser(user_id)
    bot_user.deposit(blackjack.winnings)

    await message.reply(get_final_game_update_message(user_id, blackjack))
