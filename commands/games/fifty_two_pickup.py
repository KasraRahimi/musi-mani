from enum import StrEnum
from interactions import slash_command, SlashContext, ActionRow, Button, ButtonStyle, Message
from commands.games.constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION
from games.fifty_two_pickup import FiftyTwoPickup

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

async def handle_no_input(ctx: SlashContext, msg: Message) -> None:
    pass


async def get_initial_message(ctx: SlashContext, fifty_two_pickup_game: FiftyTwoPickup) -> Message:
    pass


async def get_player_choice(ctx: SlashContext, msg: Message) -> PlayerChoice | None:
    pass


async def update_game_message(ctx: SlashContext, msg: Message, fifty_two_pickup_game: FiftyTwoPickup) -> None:
    pass


async def handle_end_game(ctx: SlashContext, msg: Message, fifty_two_pickup_game: FiftyTwoPickup) -> None:
    pass


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="fifty-two-pickup",
    sub_cmd_description="Place a bet to play a classic game of 52 pickup",
    options=[BET_OPTION]
)
async def fifty_two_pickup(ctx: SlashContext, bet: int):
    fifty_two_pickup_game = FiftyTwoPickup(bet)
    msg = await get_initial_message(ctx, fifty_two_pickup_game)

    while fifty_two_pickup_game.outcome is not None:
        player_choice = await get_player_choice(ctx, msg)
        match player_choice:
            case PlayerChoice.PICK_UP:
                fifty_two_pickup_game.pick_up_card()
            case PlayerChoice.GIVE_UP:
                fifty_two_pickup_game.give_up()
            case None:
                await handle_no_input(ctx, msg)

        await update_game_message(ctx, msg, fifty_two_pickup_game)

    await handle_end_game(ctx, msg, fifty_two_pickup_game)
