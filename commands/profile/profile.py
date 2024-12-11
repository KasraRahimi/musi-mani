from dataclasses import dataclass, asdict
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

def separate_game_stats_to_dict(game_stats: list[GameStat]) -> dict[str, list[GameStat]]:
    game_stat_dict = dict()
    for game_stat in game_stats:
        if game_stat.name not in game_stat_dict:
            game_stat_dict[game_stat.name] = [game_stat]
        else:
            game_stat_dict[game_stat.name].append(game_stat)
    return game_stat_dict

def summarize_game_stats(game_stats: list[GameStat]) -> GameStatsSummary:
    summary = GameStatsSummary()
    for game_stat in game_stats:
        summary.add_game_stat(game_stat)
    return summary

def get_game_stats_embed_fields(game_stats: list[GameStat], is_include_total: bool=False) -> list[EmbedField]:
    embed_fields: list[EmbedField] = []
    game_stats_dict = separate_game_stats_to_dict(game_stats)

    # TODO: implement logic to make in include total work.

    for name, game_stats in game_stats_dict.items():
        summary = summarize_game_stats(game_stats)

        field_value = []
        for title, stat in asdict(summary).items():
            title = title.replace("_", " ")
            field_value.append(f"{title}: **{stat}**")
        field_value = "\n".join(field_value)

        embed_fields.append(
            EmbedField(
                name=name,
                value=field_value,
                inline=True
            )
        )

    return embed_fields



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
    if user.bot:
        await ctx.send("Now why would a bot have a profile?", ephemeral=True)
        return
    bot_user = BotUser(str(user.id))

    name = bot_user.name or user.username
    description = bot_user.description
    image = EmbedAttachment(url=user.avatar_url)

    game_stats = bot_user.game_stats
    embed_fields = [
        EmbedField(name='Balance', value=f"{bot_user.balance} talan", inline=False),
        *get_game_stats_embed_fields(game_stats),
    ]

    embed = Embed(
        title=f"{name}'s profile",
        description=description,
        thumbnail=image,
        color=get_random_color(),
        fields=embed_fields,
    )
    await ctx.send(embed=embed)


