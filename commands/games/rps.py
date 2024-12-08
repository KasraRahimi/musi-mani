from enum import StrEnum
from random import randint
from interactions import slash_command, SlashContext, Message, ActionRow, Button, ButtonStyle
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet

class Choice(StrEnum):
    ROCK = 'rock',
    PAPER = 'paper',
    SCISSORS = 'scissors',

class Outcome(StrEnum):
    WIN = 'win',
    LOSE = 'lose',
    TIE = 'tie'

def get_action_row() -> list[ActionRow]:
    return [ActionRow(
        Button(
            custom_id=Choice.ROCK,
            emoji='🪨',
            label=Choice.ROCK.capitalize(),
            style=ButtonStyle.PRIMARY
        ),
        Button(
            custom_id=Choice.PAPER,
            emoji='📄',
            label=Choice.PAPER.capitalize(),
            style=ButtonStyle.GREEN,
        ),
        Button(
            custom_id=Choice.SCISSORS,
            emoji='✂️',
            label=Choice.SCISSORS.capitalize(),
            style=ButtonStyle.SECONDARY
        )
    )]


def outcome_for_rock(other: Choice) -> Outcome:
    match other:
        case Choice.PAPER:
            return Outcome.LOSE
        case Choice.SCISSORS:
            return Outcome.WIN
        case Choice.ROCK:
            return Outcome.TIE

def outcome_for_paper(other: Choice) -> Outcome:
    match other:
        case Choice.PAPER:
            return Outcome.TIE
        case Choice.SCISSORS:
            return Outcome.LOSE
        case Choice.ROCK:
            return Outcome.WIN

def outcome_for_scissors(other: Choice) -> Outcome:
    match other:
        case Choice.PAPER:
            return Outcome.WIN
        case Choice.SCISSORS:
            return Outcome.TIE
        case Choice.ROCK:
            return Outcome.LOSE

def player_1_outcome(player_1_choice: Choice, player_2_choice: Choice) -> Outcome:
    match player_1_choice:
        case Choice.PAPER:
            return outcome_for_paper(player_2_choice)
        case Choice.SCISSORS:
            return outcome_for_scissors(player_2_choice)
        case Choice.ROCK:
            return outcome_for_rock(player_2_choice)

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
    pass


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