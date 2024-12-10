from random import randint
from interactions import slash_command, SlashContext, Embed, Color, EmbedField, EmbedAttachment, SlashCommandOption, \
    OptionType, User, Member
from requests import get
from database import BotUser

# BASE_URL = "https://api.quotable.io"

USER_OPTION = SlashCommandOption(
    name="user",
    description="The user whose profile you wish to see. If none, you'll see yours",
    type=OptionType.USER,
    required=False
)

# def get_random_quote() -> str:
#     for _ in range(3):
#         response = get(f"{BASE_URL}/quotes/random", verify=False)
#         if response.status_code != 200:
#             continue
#         return response.json().pop()["content"]
#     return "No description"

def get_random_color() -> Color:
    red = randint(0, 255)
    green = randint(0, 255)
    blue = randint(0, 255)
    return Color((red, green, blue))

@slash_command(
    name="profile",
    description="See your user profile with the bot",
    options=[USER_OPTION]
)
async def profile(ctx: SlashContext, user: User | Member | None=None):
    user = user or ctx.author
    bot_user = BotUser(str(user.id))

    name = bot_user.name or user.username
    description = bot_user.description
    image = EmbedAttachment(url=user.avatar_url)

    embed = Embed(
        title=f"{name}'s profile",
        description=description,
        thumbnail=image,
        color=get_random_color(),
        fields=[EmbedField(name='Balance', value=f"{bot_user.balance} talan", inline=False)],
    )
    await ctx.send(embed=embed)


