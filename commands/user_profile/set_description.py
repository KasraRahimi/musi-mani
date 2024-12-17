from interactions import slash_command, SlashCommandOption, OptionType, SlashContext

from database import BotUser

description_option = SlashCommandOption(
    name="description",
    type=OptionType.STRING,
    required=True,
    min_length=1,
    max_length=128,
)


@slash_command(
    name="set-description",
    description="Set your profile description.",
    options=[description_option],
)
async def set_description(ctx: SlashContext, description: str):
    bot_user = BotUser(str(ctx.author.id))
    bot_user.set_description(description)
    await ctx.send("You've updated your description", ephemeral=True)
