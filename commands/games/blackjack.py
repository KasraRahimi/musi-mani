from interactions import SlashCommand, InteractionContext, Button, ButtonStyle, ActionRow
from enum import Enum

class Choice(Enum):
    HIT = 'hit'
    STAND = 'stand'
    DOUBLE = 'double'

def get_choice_action_row(has_double=False):
    hit = Button(
        custom_id=Choice.HIT.value,
        style=ButtonStyle.PRIMARY,
        label="Hit"
    )
    stand = Button(
        custom_id=Choice.STAND.value,
        style=ButtonStyle.SECONDARY,
        label="Stand"
    )
    double = Button(
        custom_id=Choice.DOUBLE.value,
        style=ButtonStyle.DANGER,
        label="Double"
    )
    if has_double:
        action_row = ActionRow(hit, stand, double)
    else:
        action_row = ActionRow(hit, stand)

    return [action_row]

async def callback(ctx: InteractionContext):
    pass

blackjack = SlashCommand(
    name="name",
    description="Replies with your name",
    callback=callback
)