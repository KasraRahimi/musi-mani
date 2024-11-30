from interactions import SlashContext, SlashCommand

async def callback(ctx: SlashContext):
    await ctx.send("🏓 pong")

ping = SlashCommand(
    name="ping",
    description="Replies with pong",
    callback=callback
)