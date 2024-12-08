from interactions import slash_command, Button, ButtonStyle, SlashContext

DOCS_BUTTON = Button(
    style=ButtonStyle.LINK,
    url="https://kawa-4.gitbook.io/musi-mani",
    label="Documentation",
)

@slash_command(
    name="help",
    description="send a help message to help explain how to use the bot",
)
async def help(ctx: SlashContext):
    content = (
        "Hi, :wave:",
        "I'm ilo musi, I'm a discord gambling bot. I offer a variety of casino games you can bet talan on. I will have a more useful help message soon. For now, refer to my documentation with the link below."
    )
    content = "\n".join(content)
    await ctx.send(content, components=DOCS_BUTTON)