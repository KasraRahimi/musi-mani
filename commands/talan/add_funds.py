from interactions import SlashCommandOption, OptionType, slash_command, check, is_owner, InteractionContext
from interactions.client.errors import CommandCheckFailure

from database import BotUser
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
    await ctx.defer()
    jan_kawa = BotUser(str(ctx.user.id))
    jan_kawa.deposit(amount)
    await ctx.send(f"I just deposited {amount} talan into your account\nYour balance: __**{jan_kawa.balance}**__ talan")