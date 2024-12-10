from interactions import slash_command, SlashContext, Embed, Color, EmbedField, EmbedAttachment


@slash_command(
    name="profile",
    description="See your user profile with the bot"
)
async def profile(ctx: SlashContext):
    image = EmbedAttachment(url=ctx.author.avatar_url)
    embed = Embed(
        title=ctx.author.display_name,
        thumbnail=image,
        color=Color((0, 255, 0)),
        description=f"{ctx.author.display_name}'s profile",
        fields=[EmbedField(name='hi', value="hello", inline=False)],
    )
    await ctx.send(embed=embed)
