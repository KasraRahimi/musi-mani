from interactions import SlashCommand, SlashContext, ActionRow, Button, ButtonStyle, Message, listen
from enum import Enum

from interactions.api.events import Component


class Choice(Enum):
    YES = 'yes'
    NO = 'no'

action_row = [
    ActionRow(
        Button(
            custom_id=Choice.YES.value,
            style=ButtonStyle.GREEN,
            label="Yes"
        ),
        Button(
            custom_id=Choice.NO.value,
            style=ButtonStyle.RED,
            label="No"
        )
    )
]

async def callback(ctx: SlashContext):
    name = ctx.author.username
    nickname = ctx.author.nickname,
    bot = ctx.bot

    if nickname is None or name == nickname:
        await ctx.send(f"Your name is simply {name}")
        return

    await ctx.send(f"Your name is {name}, though here, we call you {nickname}")

    message = await ctx.send("Did I get that right?", ephemeral=True, components=action_row)

    try:
        used_component: Component = await bot.wait_for_component(components=action_row, timeout=30)
    except TimeoutError:
        await ctx.edit(message, content="Oops, you took too long to answer", components=[])
    else:
        match used_component.ctx.custom_id:
            case Choice.YES.value:
                await ctx.send("I'm glad!", ephemeral=True)
            case Choice.NO.value:
                await ctx.send("That's a shame", ephemeral=True)

        await ctx.edit(message, components=[])

name = SlashCommand(
    name="name",
    description="Replies with your name",
    callback=callback
)