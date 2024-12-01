from interactions import SlashCommand, InteractionContext, Button, ButtonStyle, ActionRow, SlashCommandOption, \
    OptionType, Client, Message, ComponentContext
from enum import Enum

from interactions.api.events import Component

from games.blackjack import Blackjack, Outcome

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

bet = SlashCommandOption(
    name="bet",
    description="The bet you wish to place on the game",
    required=True,
    type=OptionType.INTEGER,
    min_value=0
)

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

async def get_component_ctx(bot: Client, action_row) -> None | ComponentContext:
    try:
        used_component: Component = await bot.wait_for_component(components=action_row, timeout=30)
    except TimeoutError:
        return None
    else:
        return used_component.ctx

async def callback(ctx: InteractionContext, bet: int):
    bot: Client = ctx.bot
    userId = str(ctx.author.id)
    blackjack = Blackjack(bet)

    blackjack.start()
    action_row = get_choice_action_row()
    message = await ctx.send(get_game_update_message(userId, blackjack), components=action_row)

    while blackjack.outcome is None:
        component_ctx = await get_component_ctx(bot, action_row)
        if component_ctx is None:
            await message.edit(content="You failed to reply in time", components=[])
            return

        match component_ctx.custom_id:
            case Choice.HIT.value:
                blackjack.hit()
            case Choice.STAND.value:
                blackjack.stand()
        await component_ctx.edit_origin(content=get_game_update_message(userId, blackjack), components=action_row)

    await ctx.edit(message, components=[])
    await message.reply(get_final_game_update_message(userId, blackjack))


blackjack = SlashCommand(
    name="blackjack",
    description="Play a game of blackhack",
    callback=callback,
    options=[bet]
)