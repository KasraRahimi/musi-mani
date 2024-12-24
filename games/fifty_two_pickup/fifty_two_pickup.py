from enum import StrEnum
from random import shuffle
from games.utils import Card, Rank, Suit

class Outcome(StrEnum):
    ALL_PICKED_UP = "all picked up"
    GAME_QUIT = "game quit"

DECK_SIZE = 52

class FiftyTwoPickup:
    def __init__(self, bet: int, bonus: int=100):
        self.bet = bet
        self.bonus = bonus
        self.deck = self.__get_shuffled_deck()
        self.outcome = None

    def __get_shuffled_deck(self):
        deck = [Card(rank, suit) for rank in Rank for suit in Suit]
        shuffle(deck)
        return deck

    def get_current_card(self) -> Card | None:
        if len(self.deck) > 0:
            return self.deck[-1]
        return None

    def pick_up_card(self):
        if self.outcome is not None:
            return
        self.deck.pop()
        if len(self.deck) == 0:
            self.outcome = Outcome.ALL_PICKED_UP

    def give_up(self):
        if self.outcome is not None:
            return
        self.outcome = Outcome.GAME_QUIT

    @property
    def winnings(self) -> int:
        max_win = self.bet + self.bonus
        current_return_ration = (DECK_SIZE - len(self.deck)) / DECK_SIZE
        return int(current_return_ration * max_win)

if __name__ == "__main__":
    pass