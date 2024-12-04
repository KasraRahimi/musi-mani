from interactions import slash_command, InteractionContext

from .constants import COMMAND_NAME, COMMAND_DESCRIPTION


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="daily",
    sub_cmd_description="claim your daily talan reward"
)
async def reward(ctx: InteractionContext):
    pass