import datetime

from interactions import slash_command, InteractionContext

from database import BotUser
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION

REWARD_AMOUNT = 1000
TIME_BETWEEN_CLAIMS = datetime.timedelta(days=1)

@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="daily",
    sub_cmd_description="claim your daily talan reward"
)
async def reward(ctx: InteractionContext):
    bot_user = BotUser(str(ctx.author.id))
    can_claim_again = (TIME_BETWEEN_CLAIMS - bot_user.time_since_last_reward()).total_seconds() < 0

    if can_claim_again or bot_user.last_reward is None:
        bot_user.deposit(REWARD_AMOUNT)
        await ctx.send(f"You just claimed your daily reward of {REWARD_AMOUNT} talan")
        return

    next_claim_epoch = (bot_user.last_reward + TIME_BETWEEN_CLAIMS).timestamp()
    message = (
        f"You claimed your last reward <t:{bot_user.last_reward.timestamp()}:R>",
        "",
        f"You can claim again in <t:{next_claim_epoch}:R>, that is to say <t:{next_claim_epoch}>"
    )
    message = "\n".join(message)
    await ctx.send(message)