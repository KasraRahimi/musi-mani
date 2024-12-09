from .misc import name, ping, anonymous, help
from .games import blackjack, coin_toss, last_call, rps
from .talan import balance, add_funds, give, reward, weka_ale
from .profile import profile, set_description, set_name

__all__ = [
    # misc commands
    'name',
    'ping',
    'anonymous',
    'help',
    # profile
    'profile',
    'set_description',
    'set_name',
    # games
    'blackjack',
    'coin_toss',
    'last_call',
    'rps',
    # talan
    'balance',
    'add_funds',
    'give',
    'reward',
    'weka_ale'
]