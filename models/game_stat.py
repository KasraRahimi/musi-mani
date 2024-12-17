from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Self


@dataclass
class GameStat:
    name: str
    date: datetime
    bet: int
    payout: int
    is_win: bool

    @classmethod
    def from_json(cls, json: dict) -> Self | None:
        try:
            return cls(
                name=json["name"],
                date=json["date"],
                bet=json["bet"],
                payout=json["payout"],
                is_win=json["is_win"],
            )
        except KeyError:
            return None

    def to_json(self) -> dict:
        return asdict(self)
