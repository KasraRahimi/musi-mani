from enum import StrEnum
from interactions import slash_command, SlashContext
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION, BET_OPTION, can_player_bet

class Choice(StrEnum):
    ROCK = 'rock',
    PAPER = 'paper',
    SCISSORS = 'scissors',

class Outcome(StrEnum):
    WIN = 'win',
    LOSE = 'lose',
    TIE = 'tie'

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