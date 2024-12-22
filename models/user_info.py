from dataclasses import dataclass
from datetime import datetime
from typing import Self

from constants import DATE_FORMAT
from models.game_stat import GameStat

@dataclass
class UserInfo:
    id: int
    last_reward: datetime | None
    balance: int
    name: str | None
    description: str | None
    game_stats: list[GameStat] | None

    @classmethod
    def from_json(cls, json: dict) -> Self:
        id = int(json.get("_id"))
        last_reward = json.get("last_reward")
        balance = json.get("balance")
        name = json.get("name")
        description = json.get("description")
        tmp_game_stats = json.get("game_stats")
        if tmp_game_stats:
            game_stats = [GameStat.from_json(game_stat, id) for game_stat in tmp_game_stats]
        else:
            game_stats = None

        return cls(id, last_reward, balance, name, description, game_stats)

    def to_sql_tuple(self) -> tuple:
        """
        Return a tuple of the form
        ID, NAME, DESCRIPTION, BALANCE, LAST_REWARD
        """
        if self.last_reward:
            last_reward_value = self.last_reward.strftime(DATE_FORMAT)
        else:
            last_reward_value = None
        return (
            self.id,
            self.name,
            self.description,
            self.balance,
            last_reward_value
        )

    @classmethod
    def from_sql_tuple(cls, sql_tuple: tuple, game_stats: list[GameStat]=None) -> Self:
        """
        Get a UserInfo object from a SQL SELECT query tuple
        :param sql_tuple: a tuple of the form (ID, NAME, DESCRIPTION, BALANCE, LAST_REWARD)
        :param game_stats: a list of GameStat objects
        :return: a UserInfo object
        """
        id, name, description, balance, last_reward = sql_tuple
        return cls(
            id=id,
            last_reward=last_reward,
            balance=balance,
            name=name,
            description=description,
            game_stats=game_stats
        )


