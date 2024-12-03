from interactions import SlashCommandOption, OptionType, slash_command, check, is_owner, InteractionContext
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION

AMOUNT = SlashCommandOption(
    name="amount",
    description="the amount of funds to add",
    type=OptionType.INTEGER,
    min_value=0,
    required=True,
)

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="add-funds",
    sub_cmd_description="add funds to your account",
    options=[AMOUNT]
)
@check(is_owner())
async def add_funds(ctx: InteractionContext, amount: int):
    await ctx.send("hi kawa")