from interactions import slash_command, SlashContext


@slash_command(
    name="profile",
    description="See your user profile with the bot"
)
async def profile(ctx: SlashContext):
    pass
