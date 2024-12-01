from enum import Enum

class Rank(Enum):
    ONE = "1"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"

class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank, self.suit = rank, suit

    @property
    def value(self):
        if self.rank == Rank.ACE:
            return 1
        try:
            return int(self.rank.value)
        except ValueError:
            return 10

    def __str__(self):
        return f"{self.rank.value} of {self.suit.value}"

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    deck = []
    for suit in Suit:
        for rank in Rank:
            deck.append(Card(rank, suit))
    for card in deck:
        print(f"{card} with value of {card.value}")