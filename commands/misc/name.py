from interactions import SlashContext, ActionRow, Button, ButtonStyle, Message, listen, slash_command
from enum import Enum
from interactions.api.events import Component
from asyncio import exceptions


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

@slash_command(name="name", description="Replies with your name")
async def name(ctx: SlashContext):
    username = ctx.author.username
    nickname = ctx.author.nickname
    bot = ctx.bot

    if nickname is None or username == nickname:
        await ctx.send(f"Your name is simply {username}")
        return

    await ctx.send(f"Your name is {username}, though here, we call you {nickname}")

    message = await ctx.send("Did I get that right?", ephemeral=True, components=action_row)

    try:
        used_component: Component = await bot.wait_for_component(components=action_row, timeout=30)
    except exceptions.TimeoutError:
        await ctx.edit(message, content="Oops, you took too long to answer", components=[])
    else:
        match used_component.ctx.custom_id:
            case Choice.YES.value:
                await ctx.send("I'm glad!", ephemeral=True)
            case Choice.NO.value:
                await ctx.send("That's a shame", ephemeral=True)

        await ctx.edit(message,components=[])
