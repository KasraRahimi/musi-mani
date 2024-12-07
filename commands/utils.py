from dataclasses import dataclass
from interactions import SlashContext

SEPERATOR = "."

def get_button_id(value: str, ctx: SlashContext):
    button_id = map(str, (value, ctx.id, ctx.author.id))
    return SEPERATOR.join(button_id)

@dataclass
class ButtonIdInfo:
    value: str
    ctx_id: str
    user_id: str

    def __init__(self, button_id: str):
        button_info = button_id.split(SEPERATOR)
        if len(button_info) != 3:
            raise ValueError("button id must have three elements")
        self.value = button_info[0]
        self.ctx_id = button_info[1]
        self.user_id = button_info[2]