from asyncio import exceptions, sleep
from enum import StrEnum
from random import randint
from interactions import slash_command, SlashContext, Message, ActionRow, Button, ButtonStyle
from interactions.api.events import Component
from dataclasses import dataclass
from database import BotUser
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet

WIN_MULTIPLIER = 2

class Choice(StrEnum):
    ROCK = 'rock',
    PAPER = 'paper',
    SCISSORS = 'scissors',

class Outcome(StrEnum):
    PLAYER_ONE_WIN = 'player_one_win'
    PLAYER_TWO_WIN = 'player_two_win'
    TIE = 'tie'

@dataclass
class RpsGameState:
    player_one_choice: Choice | None = None
    player_two_choice: Choice | None = None
    bet: int = 0

    __WIN_MULTIPLIER = 2

    def __init__(self, bet: int):
        self.bet = bet

    @property
    def outcome(self) -> Outcome | None:
        if self.player_one_choice is None or self.player_two_choice is None:
            return None

        if self.player_one_choice == self.player_two_choice:
            return Outcome.TIE

        match (self.player_one_choice, self.player_two_choice):
            case (Choice.ROCK, second_choice):
                match second_choice:
                    case Choice.PAPER:
                        return Outcome.PLAYER_TWO_WIN
                    case Choice.SCISSORS:
                        return  Outcome.PLAYER_ONE_WIN

            case (Choice.PAPER, second_choice):
                match second_choice:
                    case Choice.ROCK:
                        return Outcome.PLAYER_ONE_WIN
                    case Choice.SCISSORS:
                        return Outcome.PLAYER_TWO_WIN

            case (Choice.SCISSORS, second_choice):
                match second_choice:
                    case Choice.ROCK:
                        return Outcome.PLAYER_TWO_WIN
                    case Choice.PAPER:
                        return Outcome.PLAYER_ONE_WIN

    @property
    def player_one_winnings(self) -> int:
        match self.outcome:
            case Outcome.PLAYER_ONE_WIN:
                return self.bet ** self.__WIN_MULTIPLIER
            case Outcome.TIE:
                return self.bet
            case Outcome.PLAYER_TWO_WIN:
                return 0
            case _:
                return 0

    @property
    def player_two_winnings(self) -> int:
        match self.outcome:
            case Outcome.PLAYER_ONE_WIN:
                return 0
            case Outcome.TIE:
                return self.bet
            case Outcome.PLAYER_TWO_WIN:
                return self.bet ** self.__WIN_MULTIPLIER
            case _:
                return 0


def get_emoji_from_choice(choice: Choice) -> str:
    match choice:
        case Choice.ROCK:
            return '🪨'
        case Choice.PAPER:
            return '📄'
        case Choice.SCISSORS:
            return '✂️'

def get_action_row() -> list[ActionRow]:
    return [ActionRow(
        Button(
            custom_id=Choice.ROCK,
            emoji=get_emoji_from_choice(Choice.ROCK),
            label=Choice.ROCK.capitalize(),
            style=ButtonStyle.PRIMARY
        ),
        Button(
            custom_id=Choice.PAPER,
            emoji=get_emoji_from_choice(Choice.PAPER),
            label=Choice.PAPER.capitalize(),
            style=ButtonStyle.GREEN,
        ),
        Button(
            custom_id=Choice.SCISSORS,
            emoji=get_emoji_from_choice(Choice.SCISSORS),
            label=Choice.SCISSORS.capitalize(),
            style=ButtonStyle.SECONDARY
        )
    )]

def get_random_choice() -> Choice:
    random_number = randint(1, 3)
    match random_number:
        case 1:
            return Choice.PAPER
        case 2:
            return Choice.SCISSORS
        case 3:
            return Choice.ROCK

def get_message_title(ctx: SlashContext) -> str:
    user_id = str(ctx.author.id)
    content = (
        "### Rock Paper Scissors",
        f"<@{user_id}>'s game",
        ""
    )
    return "\n".join(content)

async def get_initial_message(ctx: SlashContext) -> Message:
    content = (
        get_message_title(ctx),
        "Pick an option",
    )
    content = '\n'.join(content)
    return await ctx.send(content, components=get_action_row())

async def get_player_choice(ctx: SlashContext, msg: Message) -> Choice | None:
    async def check(component_event: Component) -> bool:
        if component_event.ctx.author.id == ctx.author.id:
            return True
        else:
            await component_event.ctx.edit_origin()
            return False

    try:
        used_component: Component = await ctx.bot.wait_for_component(components=get_action_row(), messages=msg, timeout=30)
    except exceptions.TimeoutError:
        return None
    else:
        content = (
            get_message_title(ctx),
            "Waiting for bot choice..."
        )
        content = '\n'.join(content)
        await used_component.ctx.edit_origin(content=content, components=[])
        return Choice(used_component.ctx.custom_id)

async def handle_game_end(ctx: SlashContext, msg: Message, rps_game_state: RpsGameState) -> None:
    content = [
        get_message_title(ctx),
        f"The bot picked {rps_game_state.player_two_choice} ({get_emoji_from_choice(rps_game_state.player_two_choice)})"
    ]

    match rps_game_state.outcome:
        case Outcome.PLAYER_ONE_WIN:
            content.append(f"You won! You've been awarded {rps_game_state.player_one_winnings} talan!")
        case Outcome.PLAYER_TWO_WIN:
            content.append(f"You lost.")
        case Outcome.TIE:
            content.append(f"It's a tie. You've been given back {rps_game_state.player_one_winnings} talan")

    BotUser(str(ctx.author.id)).deposit(rps_game_state.player_one_winnings)

    content = '\n'.join(content)
    await ctx.edit(msg, content=content, components=[])



@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="rps",
    sub_cmd_description="place a bet on a game of rock paper scissors",
    options=[BET_OPTION]
)
async def rps(ctx: SlashContext, bet: int):
    if not can_player_bet(ctx, bet, do_withdraw=True):
        await ctx.send("You do not have enough talan to place this bet.", ephemeral=True)
        return

    rps_game_state = RpsGameState()
    msg = await get_initial_message(ctx)

    player_choice = await get_player_choice(ctx, msg)
    await sleep(1.0)
    if player_choice is None:
        await ctx.edit(msg, content="You failed to reply in time", components=[])
        return
    rps_game_state.player_one_choice = player_choice

    bot_choice = get_random_choice()
    rps_game_state.player_two_choice = bot_choice
    await handle_game_end(ctx, msg, rps_game_state)
