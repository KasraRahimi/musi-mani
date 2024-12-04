from interactions import SlashCommandOption, OptionType, SlashContext

from database import BotUser

COMMAND_NAME = "play"

COMMAND_DESCRIPTION = "Place a bet on a casino game"

BET_OPTION = SlashCommandOption(
    name="bet",
    description="The bet you wish to place on the game",
    required=True,
    type=OptionType.INTEGER,
    min_value=0
)

INSUFFICIENT_FUNDS_MSG = "You do not have enough talan to place that bet"


def can_player_bet(ctx: SlashContext, bet: int, do_withdraw: bool = True):
    user_id = str(ctx.author.id)
    bot_user = BotUser(user_id)

    # simply check if the user has enough funds for the bet
    if not do_withdraw:
        return bot_user.balance >= bet

    # try to withdraw, and if it fails, tell user they don't have enough
    try:
        bot_user.withdraw(bet)
    except ValueError:
        return False
    else:
        return True
