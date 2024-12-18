from enum import Enum
from .card import Card, Rank, Suit
from random import shuffle


class Outcome(Enum):
    BLACKJACK = 0
    WIN = 1
    LOSE = 2
    DRAW = 3


def get_hand_value(deck: list[Card]) -> int:
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


class Blackjack:
    WIN_MULTIPLIER = 2
    BLACKJACK_MULTIPLIER = 2.5

    def __init__(self, bet: int, num_of_decks: int = 2):
        self.outcome: None | Outcome = None
        self.bet: int = bet
        self.deck: list[Card] = self.__get_shuffled_deck(num_of_decks)
        self.can_double: bool = True

        self.player_hand: list[Card] = []
        self.dealer_hand: list[Card] = []

    @classmethod
    def get_deck(cls) -> list[Card]:
        return [Card(rank, suit) for suit in Suit for rank in Rank]

    def __get_shuffled_deck(self, num_of_decks) -> list[Card]:
        deck = self.get_deck() * num_of_decks
        shuffle(deck)
        return deck

    @property
    def player_value(self) -> int:
        return get_hand_value(self.player_hand)

    @property
    def dealer_value(self) -> int:
        return get_hand_value(self.dealer_hand)

    @property
    def dealer_first_card(self) -> Card | None:
        if len(self.dealer_hand) < 1:
            return None
        return self.dealer_hand[0]

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
        if self.outcome is not None:
            return

        self.can_double = False
        self.player_hand.append(self.deck.pop())

        if self.player_value > 21:
            self.outcome = Outcome.LOSE

    def stand(self):
        if self.outcome is not None:
            return

        self.can_double = False

        while self.dealer_value < 17:
            self.dealer_hand.append(self.deck.pop())

        if self.dealer_value > 21 or self.dealer_value < self.player_value:
            self.outcome = Outcome.WIN
            return
        if self.dealer_value > self.player_value:
            self.outcome = Outcome.LOSE
            return
        if self.dealer_value == self.player_value:
            self.outcome = Outcome.DRAW
            return

    def double(self):
        if self.outcome is not None or not self.can_double:
            return

        self.bet *= 2
        self.hit()
        self.stand()

    @property
    def winnings(self):
        winnings = 0
        match self.outcome:
            case Outcome.WIN:
                winnings = self.bet * self.WIN_MULTIPLIER
            case Outcome.LOSE:
                winnings = 0
            case Outcome.BLACKJACK:
                winnings = self.bet * self.BLACKJACK_MULTIPLIER
            case Outcome.DRAW:
                winnings = self.bet
        return int(winnings)


# def get_player_input() -> int:
#     print("1 - hit")
#     print("2 - stand")
#     return int(input("> "))
#
# def print_cards(hand: list[Card]):
#     for card in hand:
#         print("• {}".format(card))
#
# if __name__ == "__main__":
#     print("== Blackjack ==")
#     blackjack = Blackjack(100)
#     blackjack.start()
#     while blackjack.outcome is None:
#         print("Dealers first card: {}".format(blackjack.dealer_first_card))
#         print("\n~ your cards ~")
#         print_cards(blackjack.player_hand)
#         print(f"Value: {blackjack.player_value}\n")
#         choice = get_player_input()
#         match choice:
#             case 1:
#                 blackjack.hit()
#             case 2:
#                 blackjack.stand()
#             case 3:
#                 break
#     print("~~ Dealer's final cards ~~")
#     print_cards(blackjack.dealer_hand)
#     print("value: {}".format(blackjack.dealer_value))
#     print("\n~~ Player's final cards ~~")
#     print_cards(blackjack.player_hand)
#     print(f"value: {blackjack.player_value}")
#     print("Outcome: {}".format(blackjack.outcome))
