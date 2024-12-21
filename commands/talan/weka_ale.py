from interactions import (
    slash_command,
    SlashContext,
    ActionRow,
    Button,
    ButtonStyle,
    check,
    is_owner,
)
from interactions.api.events import Component
from asyncio import exceptions

from database.sql_db import SQLDb
from .constants import COMMAND_NAME, COMMAND_DESCRIPTION
from enum import Enum


class Choice(Enum):
    YES = "yes"
    NO = "no"


ACTION_ROW = [
    ActionRow(
        Button(custom_id=Choice.YES.value, style=ButtonStyle.GREEN, label="WILE"),
        Button(custom_id=Choice.NO.value, style=ButtonStyle.RED, label="ALA"),
    )
]


async def get_owner_confirmation(ctx: SlashContext) -> None | str:
    msg = await ctx.send(
        "sina pali e ni la mani ale pi jan ale li weka. ona li weka la ona li ken ala kama sin\nsina __**wile ala wile**__ pali e ni?",
        components=ACTION_ROW,
    )

    async def is_same_user_check(component: Component):
        if component.ctx.author.id == ctx.author.id:
            return True
        await component.ctx.edit_origin()
        return False

    try:
        used_component: Component = await ctx.bot.wait_for_component(
            components=ACTION_ROW, messages=msg, timeout=60, check=is_same_user_check
        )
    except exceptions.TimeoutError:
        await msg.edit(components=[])
        return None
    else:
        await used_component.ctx.edit_origin(components=[])
        return used_component.ctx.custom_id


async def delete_all_account(ctx: SlashContext):
    db = SQLDb()
    delete_count = db.reset_all_data()
    await ctx.send("mi weka e mani ale. mani pi jan {} li weka".format(delete_count))


@slash_command(
    name=COMMAND_NAME,
    description=COMMAND_DESCRIPTION,
    sub_cmd_name="weka-ale",
    sub_cmd_description="sina kepeken e ni la mani pi jan ale li weka",
)
@check(is_owner())
async def weka_ale(ctx: SlashContext):
    owner_choice = await get_owner_confirmation(ctx)
    match owner_choice:
        case Choice.YES.value:
            await delete_all_account(ctx)
        case Choice.NO.value:
            await ctx.send("ni la mani ale li awen lon")
        case None:
            await ctx.send(
                "mi sukumen e toki sina, taso sina toki ala. ni la mi pini e ken sina."
            )
