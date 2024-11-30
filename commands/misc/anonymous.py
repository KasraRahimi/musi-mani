from interactions import SlashContext, SlashCommand, SlashCommandOption, OptionType, Member

user_option = SlashCommandOption(
    name="user",
    description="the user to anonymously message",
    required=True,
    type=OptionType.USER
)

content_option = SlashCommandOption(
    name="content",
    description="the content of the anonymous message",
    required=True,
    type=OptionType.STRING
)

async def callback(ctx: SlashContext, user: Member, content: str):
    await ctx.send(f"I'll be sending {user.username}", ephemeral=True)
    try:
        await user.send(f"Hello, {user.username}!\n\nI'm anonymously delivering a message sent by {ctx.author.username}. The message reads as follows:\n{content}")
    except Exception as e:
        print("Error sending a message: {}".format(e))

anonymous = SlashCommand(
    name="anonymous",
    description="anonymously send a message to a friend",
    callback=callback,
    options=[user_option, content_option]
)