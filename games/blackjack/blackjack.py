from enum import Enum
from card import Card, Rank, Suit
from random import shuffle

class Outcome(Enum):
    BLACKJACK = 0
    WIN = 1
    LOSE = 2
    DRAW = 3

class Blackjack:
    def __init__(self, bet: int, num_of_decks: int=2):
        self.outcome: None | Outcome = None
        self.bet: int = bet
        self.deck: list[Card] = self.__get_shuffled_deck(num_of_decks)
        self.canDouble: bool = True

        self.player_hand, self.dealer_hand = [], []


    def __get_shuffled_deck(self, num_of_decks):
        deck = self.get_deck() * num_of_decks
        shuffle(deck)
        return deck

    @classmethod
    def get_deck(cls):
        return [Card(rank, suit) for suit in Suit for rank in Rank]

if __name__ == "__main__":
    pass