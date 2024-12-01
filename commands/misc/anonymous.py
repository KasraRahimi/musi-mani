from interactions import SlashContext, SlashCommandOption, OptionType, Member, slash_command

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

@slash_command(
    name="anonymous",
    description="anonymously send a message to a friend",
    options=[user_option, content_option]
)
async def anonymous(ctx: SlashContext, user: Member, content: str):
    await ctx.send(f"I'll be sending {user.username}", ephemeral=True)
    try:
        await user.send(f"Hello, {user.username}!\n\nI'm anonymously delivering a message sent by {ctx.author.username}. The message reads as follows:\n{content}")
    except Exception as e:
        print("Error sending a message: {}".format(e))
