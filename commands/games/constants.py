from interactions import SlashCommandOption, OptionType

COMMAND_NAME = "play"

COMMAND_DESCRIPTION = "Place a bet on a casino game"

BET_OPTION = SlashCommandOption(
    name="bet",
    description="The bet you wish to place on the game",
    required=True,
    type=OptionType.INTEGER,
    min_value=0
)
