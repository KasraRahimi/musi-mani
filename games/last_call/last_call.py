from enum import Enum
from random import random

class Outcome(Enum):
    CRASH = 'crash'
    CASH_OUT = 'cash_out'


class LastCall:

    def __init__(self, bet: int, odds_of_crash_per_iteration: float):
        self.bet = bet
        self.odds = odds_of_crash_per_iteration
        self.num_of_steps = None
        self.outcome = None

    def is_safe(self):
        return random() >= self.odds

    def step(self):
        if self.num_of_steps is None:
            self.num_of_steps = 0
            return
        if self.is_safe():
            self.num_of_steps += 1
            return
        self.outcome = Outcome.CRASH

    def cash_out(self):
        if self.outcome is None:
            self.outcome = Outcome.CASH_OUT

    @property
    def winnings(self):
        match self.outcome:
            case Outcome.CASH_OUT:
                return self.potential_winnings
            case Outcome.CRASH:
                return 0
            case _:
                return 0

    @property
    def potential_winnings(self):
        survival_odd = (1 - self.odds) ** self.num_of_steps
        bet_multiplier = 1 / survival_odd
        return self.bet * bet_multiplier
