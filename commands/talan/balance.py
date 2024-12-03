from interactions import slash_command, InteractionContext

from database import BotUser
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="balance",
    sub_cmd_description="verify your talan balance"
)
async def balance(ctx: InteractionContext):
    await ctx.defer()
    user_id = str(ctx.author.id)
    bot_user = BotUser(user_id)
    user_balance = bot_user.balance
    await ctx.send(f"Balance: __**{user_balance}**__ talan")