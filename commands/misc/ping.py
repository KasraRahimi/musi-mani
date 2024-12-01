from interactions import SlashContext, slash_command

@slash_command(
    name="ping",
    description="Replies with pong",
)
async def ping(ctx: SlashContext):
    await ctx.send("🏓 pong")
