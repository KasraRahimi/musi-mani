from interactions import SlashContext, slash_command

@slash_command(
    name="ping",
    description="Prompt the bot to reply with a pong.",
)
async def ping(ctx: SlashContext):
    await ctx.send("🏓 pong")
