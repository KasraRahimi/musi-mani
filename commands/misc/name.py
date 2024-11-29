from interactions import slash_command, SlashContext

@slash_command(name="name", description="Replies with your name")
async def name(ctx: SlashContext):
    name = ctx.author.username
    nickname = ctx.author.nickname

    if nickname is None:
        await ctx.send(f"Your name is simply {name}")
        return
    
    
    await ctx.send(f"Your name is {name}, though here, we call you {nickname}")