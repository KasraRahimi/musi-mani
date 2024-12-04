from interactions import SlashCommandOption, OptionType, slash_command, InteractionContext
from interactions.models.discord.user import Member

from commands.talan.constants import COMMAND_NAME, COMMAND_DESCRIPTION
from database import BotUser

USER = SlashCommandOption(
    name='user',
    required=True,
    description='The user to give the talan to',
    type=OptionType.USER,
)

AMOUNT = SlashCommandOption(
    name="amount",
    description="the amount of talan to give",
    type=OptionType.INTEGER,
    min_value=0,
    required=True,
)

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="give",
    sub_cmd_description="give talan to a user",
    options=[USER, AMOUNT],
)
async def give(ctx: InteractionContext, user: Member, amount: int):
    await ctx.defer()
    sender = BotUser(str(ctx.author.id))
    try:
        sender.withdraw(amount)
    except ValueError:
        await ctx.send("You do not have the funds to give that much talan")
        return
    recipient = BotUser(str(user.id))
    recipient.deposit(amount)
    await ctx.send(f"You just gave {amount} talan to <@{user.id}>")