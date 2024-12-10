from random import randint
from interactions import slash_command, SlashContext, Embed, Color, EmbedField, EmbedAttachment
from requests import get
from database import BotUser

BASE_URL = "https://api.quotable.io"

def get_random_quote() -> str:
    for _ in range(3):
        response = get(f"{BASE_URL}/quotes/random", verify=False)
        if response.status_code != 200:
            continue
        return response.json().pop()["content"]
    return "No description"

def get_random_color() -> Color:
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)
    return Color((red, green, blue))

@slash_command(
    name="profile",
    description="See your user profile with the bot"
)
async def profile(ctx: SlashContext):
    user_id = str(ctx.author.id)
    bot_user = BotUser(user_id)

    name = bot_user.name or ctx.author.username
    description = bot_user.description or get_random_quote()
    image = EmbedAttachment(url=ctx.author.avatar_url)

    embed = Embed(
        title=f"{name}'s profile",
        description=description,
        thumbnail=image,
        color=get_random_color(),
        fields=[EmbedField(name='Balance', value=f"{bot_user.balance} talan", inline=False)],
    )
    await ctx.send(embed=embed)


