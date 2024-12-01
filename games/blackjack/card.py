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
    CLUB = "club"
    DIAMOND = "diamond"
    HEART = "heart"
    SPADE = "spade"

if __name__ == "__main__":
    for suit in Suit:
        print(suit.name)