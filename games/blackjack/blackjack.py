from enum import Enum
from card import Card, Rank, Suit
from random import shuffle

class Outcome(Enum):
    BLACKJACK = 0
    WIN = 1
    LOSE = 2
    DRAW = 3

class Blackjack:
    WIN_MULTIPLIER = 2
    BLACKJACK_MULTIPLIER = 2.5

    def __init__(self, bet: int, num_of_decks: int=2):
        self.outcome: None | Outcome = None
        self.bet: int = bet
        self.deck: list[Card] = self.__get_shuffled_deck(num_of_decks)
        self.canDouble: bool = True

        self.player_hand: list[Card] = []
        self.dealer_hand: list[Card] = []

    @classmethod
    def get_deck(cls):
        return [Card(rank, suit) for suit in Suit for rank in Rank]

    def __get_shuffled_deck(self, num_of_decks):
        deck = self.get_deck() * num_of_decks
        shuffle(deck)
        return deck

    def __get_hand_value(self, deck: list[Card]):
        ace_count = 0
        total = 0
        for card in deck:
            total += card.value
            if card.rank == Rank.ACE:
                ace_count += 1

        while ace_count > 0 and total + 10 <= 21:
            total += 10
            ace_count -= 1

        return total

    @property
    def player_value(self):
        return self.__get_hand_value(self.player_hand)

    @property
    def dealer_value(self):
        return self.__get_hand_value(self.dealer_hand)

    def start(self):
        if self.outcome is not None:
            return

        for _ in range(2):
            self.player_hand.append(self.deck.pop())
        for _ in range(2):
            self.dealer_hand.append(self.deck.pop())

        if self.player_value > 21:
            self.outcome = Outcome.LOSE
            return

        if self.player_value == 21:
            if self.dealer_value == 21:
                self.outcome = Outcome.DRAW
                return
            self.outcome = Outcome.BLACKJACK

    def hit(self):
        self.canDouble = False

    def stand(self):
        self.canDouble = False

    def double(self):
        self.canDouble = False


if __name__ == "__main__":
    pass