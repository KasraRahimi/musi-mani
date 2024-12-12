from dataclasses import dataclass
from interactions import SlashContext
from typing import Self

SEPERATOR = "."

def get_button_id(value: str, ctx: SlashContext):
    button_id = map(str, (value, ctx.id, ctx.author.id))
    return SEPERATOR.join(button_id)

@dataclass
class ButtonIdInfo:
    value: str
    ctx_id: str
    user_id: str

    @classmethod
    def from_button_id(cls, button_id: str) -> Self:
        button_info = button_id.split(SEPERATOR)
        if len(button_info) != 3:
            raise ValueError("button id must have three elements")
        return cls(button_info[0], button_info[1], button_info[2])