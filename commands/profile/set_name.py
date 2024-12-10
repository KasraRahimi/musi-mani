from interactions import slash_command, SlashCommandOption, OptionType, SlashContext

from database import BotUser

NAME_OPTION = SlashCommandOption(
    name="name",
    description="The name you'd like the bot to remember you as",
    type=OptionType.STRING,
    min_length=1,
    max_length=32,
    required=True
)

@slash_command(
    name="set-name",
    description="Set your name for the bot",
    options=[NAME_OPTION]
)
async def set_name(ctx: SlashContext, name: str):
    bot_user = BotUser(str(ctx.author.id))
    bot_user.set_name(name)
    await ctx.send("You've updated your name", ephemeral=True)