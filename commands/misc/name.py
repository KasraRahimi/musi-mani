from interactions import SlashCommand, SlashContext

async def callback(ctx: SlashContext):
    name = ctx.author.username
    nickname = ctx.author.nickname

    if nickname is None:
        await ctx.send(f"Your name is simply {name}")
        return
    
    
    await ctx.send(f"Your name is {name}, though here, we call you {nickname}")

name = SlashCommand(
    name="name",
    description="Replies with your name",
    callback=callback
)