from dataclasses import dataclass
from random import randint
from interactions import slash_command, SlashContext, Embed, Color, EmbedField, EmbedAttachment, SlashCommandOption, \
    OptionType, User, Member
from requests import get
from database import BotUser
from models.game_stat import GameStat

# BASE_URL = "https://api.quotable.io"

@dataclass
class GameStatsSummary:
    total_games: int = 0
    total_wins: int = 0
    earnings: int = 0

    def add_game_stat(self, game_stat: GameStat) -> None:
        self.total_games += 1
        if game_stat.is_win:
            self.total_wins += 1
        self.earnings += game_stat.payout - game_stat.bet

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

def separate_game_stats_to_dict(game_stats: list[GameStat]) -> dict[str, GameStat]:
    game_stat_dict = dict()
    for game_stat in game_stats:
        if game_stat.name not in game_stat_dict:
            game_stat_dict[game_stat.name] = [game_stat]
        else:
            game_stat_dict[game_stat.name].append(game_stat)

def summarize_game_stats(game_stats: list[GameStat]) -> GameStatsSummary:
    summary = GameStatsSummary()
    for game_stat in game_stats:
        summary.add_game_stat(game_stat)
    return summary


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


