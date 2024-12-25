from asyncio.exceptions import TimeoutError
from datetime import datetime
from enum import StrEnum
from interactions import slash_command, SlashContext, ActionRow, Button, ButtonStyle, Message, Client
from interactions.api.events import Component

from commands.games.constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet
from database import BotUser
from games.fifty_two_pickup import FiftyTwoPickup, Outcome
from models.game_stat import GameStat

GAME_NAME = "Fifty Two Pickup"

class PlayerChoice(StrEnum):
    PICK_UP = "pick-up"
    GIVE_UP = "give-up"

BUTTONS = ActionRow(
    Button(
        style=ButtonStyle.PRIMARY,
        label="Pick up card",
        emoji="⬆️",
        custom_id=PlayerChoice.PICK_UP,
    ),
    Button(
        style=ButtonStyle.DANGER,
        label="Give up",
        emoji="👎️",
        custom_id=PlayerChoice.GIVE_UP,
    )
)

def get_message_content(ctx: SlashContext, fifty_two_pickup_game: FiftyTwoPickup) -> str:
    winnings = fifty_two_pickup_game.winnings
    current_card = fifty_two_pickup_game.get_current_card()
    user_id = str(ctx.author.id)
    content = (
        f"### {GAME_NAME}",
        f"<@{user_id}>'s game",
        "",
        "__current card__",
        f"- {current_card}",
        "",
        f"current payout: {winnings} talan",
    )
    return "\n".join(content)


async def handle_no_input(ctx: SlashContext, msg: Message) -> None:
    await ctx.edit(message=msg, components=[])
    await ctx.send("You took too long to respond.", ephemeral=True)


async def get_initial_message(ctx: SlashContext, fifty_two_pickup_game: FiftyTwoPickup) -> Message:
    return await ctx.send(
        get_message_content(ctx, fifty_two_pickup_game),
        components=[BUTTONS]
    )


async def get_player_choice(ctx: SlashContext, msg: Message) -> PlayerChoice | None:
    bot: Client = ctx.bot

    async def same_user_check(component: Component) -> bool:
        if component.ctx.author.id == ctx.author.id:
            await component.ctx.edit_origin(components=[])
            return True
        else:
            await component.ctx.edit_origin()
            return False

    try:
        component: Component = await bot.wait_for_component(messages=msg, components=BUTTONS, check=same_user_check, timeout=120)
    except TimeoutError:
        return None
    else:
        return PlayerChoice(component.ctx.custom_id)

async def update_game_message(ctx: SlashContext, msg: Message, fifty_two_pickup_game: FiftyTwoPickup) -> None:
    await ctx.edit(
        message=msg,
        content=get_message_content(ctx, fifty_two_pickup_game),
        components=[BUTTONS]
    )


async def handle_end_game(ctx: SlashContext, msg: Message, fifty_two_pickup_game: FiftyTwoPickup) -> None:
    content = f"### {GAME_NAME}\n<@{ctx.author.id}>'s game\n\n"
    match fifty_two_pickup_game.outcome:
        case Outcome.ALL_PICKED_UP:
            content += "You picked up all the cards! You win!\n"
            content += f"You've been awarded {fifty_two_pickup_game.winnings} talan!"
        case Outcome.GAME_QUIT:
            content += "Couldn't finish the game? Welp, you lost.\n"
            content += f"You've been given {fifty_two_pickup_game.winnings} talan for your efforts."
        case _:
            content = "Something went wrong. Please try again."

    bot_user = BotUser(str(ctx.author.id))
    bot_user.deposit(fifty_two_pickup_game.winnings)

    game_stat = GameStat(
        name=GAME_NAME,
        date=datetime.now(),
        bet=fifty_two_pickup_game.bet,
        payout=fifty_two_pickup_game.winnings,
        is_win=fifty_two_pickup_game.outcome == Outcome.ALL_PICKED_UP,
    )
    bot_user.add_game_stat(game_stat)
    await ctx.edit(message=msg, content=content, components=[])


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="fifty-two-pickup",
    sub_cmd_description="Place a bet to play a classic game of 52 pickup",
    options=[BET_OPTION]
)
async def fifty_two_pickup(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send("You do not have enough talan to place this bet", ephemeral=True)
        return

    fifty_two_pickup_game = FiftyTwoPickup(bet)
    msg = await get_initial_message(ctx, fifty_two_pickup_game)

    while fifty_two_pickup_game.outcome is None:
        player_choice = await get_player_choice(ctx, msg)
        match player_choice:
            case PlayerChoice.PICK_UP:
                fifty_two_pickup_game.pick_up_card()
            case PlayerChoice.GIVE_UP:
                fifty_two_pickup_game.give_up()
            case None:
                await handle_no_input(ctx, msg)
                return

        await update_game_message(ctx, msg, fifty_two_pickup_game)

    await handle_end_game(ctx, msg, fifty_two_pickup_game)

if __name__ == "__main__":
    ftp = FiftyTwoPickup(100)
    print(get_message_content(None, ftp))

