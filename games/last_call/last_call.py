from enum import Enum
from random import random

class Outcome(Enum):
    CRASH = 'crash'
    CASH_OUT = 'cash_out'


class LastCall:

    def __init__(self, bet: int, odds_of_crash_per_iteration: float):
        self.bet = bet
        self.odds = odds_of_crash_per_iteration
        self.num_of_steps = 0
        self.outcome = None

    def is_safe(self):
        return random() >= self.odds

    def step(self):
        self.num_of_steps += 1
