from .misc import name, ping, anonymous, help
from .games import blackjack, coin_toss, last_call, rps, horse_race
from .talan import balance, add_funds, give, reward, weka_ale
from .user_profile import profile, set_description, set_name

__all__ = [
    # misc commands
    "name",
    "ping",
    "anonymous",
    "help",
    # user_profile
    "profile",
    "set_description",
    "set_name",
    # games
    "blackjack",
    "coin_toss",
    "last_call",
    "rps",
    "horse_race",
    # talan
    "balance",
    "add_funds",
    "give",
    "reward",
    "weka_ale",
]
