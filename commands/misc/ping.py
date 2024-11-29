from interactions import slash_command, SlashContext

@slash_command(name="ping", description="Replies with pong")
async def ping(ctx: SlashContext):
    await ctx.send("pong")