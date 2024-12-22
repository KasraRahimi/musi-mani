from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Self

from constants import DATE_FORMAT


@dataclass
class GameStat:
    name: str
    date: datetime
    bet: int
    payout: int
    is_win: bool
    user_id: int | None=None

    @classmethod
    def from_json(cls, json: dict, user_id: int=0) -> Self | None:
        try:
            return cls(
                name=json["name"],
                date=json["date"],
                user_id=user_id,
                bet=json["bet"],
                payout=json["payout"],
                is_win=json["is_win"],
            )
        except KeyError:
            return None

    def to_json(self) -> dict:
        return asdict(self)

    def to_sql_tuple(self) -> tuple:
        """
        Return a tuple of the form
        USER_ID, NAME, DATE, BET, PAYOUT, IS_WIN
        """
        date_value = self.date.strftime(DATE_FORMAT) if self.date else None
        if not date_value:
            raise ValueError(
                "date must be a datetime object or None"
            )
        return (
            self.user_id,
            self.name,
            date_value,
            self.bet,
            self.payout,
            self.is_win
        )

    @classmethod
    def from_sql_tuple(cls, sql_tuple: tuple) -> Self:
        """
        Turn a tuple from a SQL SELECT query into a GameStat object
        :param sql_tuple: a tuple of the form (USER_ID, NAME, DATE, BET, PAYOUT, IS_WIN)
        :return: a GameStat object
        """
        user_id, name, date, bet, payout, is_win = sql_tuple
        return cls(
            name=name,
            date=date,
            user_id=user_id,
            bet=bet,
            payout=payout,
            is_win=bool(is_win)
        )
