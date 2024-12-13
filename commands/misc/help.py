from asyncio import sleep, create_task
from datetime import datetime
from dataclasses import dataclass
from enum import StrEnum
from interactions.api.events import Component
from interactions.client.utils import timestamp_converter
import commands
from interactions import slash_command, Button, ButtonStyle, SlashContext, SlashCommand, ActionRow, EmbedField, \
    ComponentContext, InteractionContext, Embed, EmbedAuthor, Message, listen, component_callback
from commands.utils import get_button_id, ButtonIdInfo

IGNORED_COMMANDS = [
    'add_funds',
    'weka_ale',
]

@dataclass
class CommandInfo:
    name: str
    description: str

    @property
    def call_name(self) -> str:
        return f"/{self.name}"

class Page(StrEnum):
    MISC_MODULE = 'misc'
    TALAN_MODULE = 'talan'
    PROFILE_MODULE = 'user_profile'
    GAMES_MODULE = 'games'

DOCS_BUTTON = ActionRow(Button(
    style=ButtonStyle.LINK,
    url="https://kawa-4.gitbook.io/musi-mani",
    label="Documentation",
    emoji='📖',
))

def get_page_changing_buttons(ctx: InteractionContext, is_disabled: bool=False) -> list[Button]:
    return [
        Button(
            style=ButtonStyle.SECONDARY,
            label="Misc",
            custom_id=get_button_id(Page.MISC_MODULE, ctx),
            emoji="🔮",
            disabled=is_disabled
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Talan",
            custom_id=get_button_id(Page.TALAN_MODULE, ctx),
            emoji="🪙",
            disabled=is_disabled
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Profile",
            custom_id=get_button_id(Page.PROFILE_MODULE, ctx),
            emoji="ℹ️",
            disabled=is_disabled
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Games",
            custom_id=get_button_id(Page.GAMES_MODULE, ctx),
            emoji="🎲",
            disabled=is_disabled
        )
    ]

def get_page_changing_action_row(ctx: InteractionContext, is_disabled: bool=False) -> ActionRow:
    return ActionRow(
        *get_page_changing_buttons(ctx, is_disabled=is_disabled)
    )

def get_command_info(cmd: SlashCommand) -> CommandInfo:
    if cmd.is_subcommand:
        name = f"{cmd.name} {cmd.sub_cmd_name}"
        description = cmd.sub_cmd_description
    else:
        name = cmd.name
        description = cmd.description
    return CommandInfo(name, str(description))


def get_command_infos_from_module(module_name: str) -> list[CommandInfo]:
    module = getattr(commands, module_name)
    command_names = module.__all__
    command_infos = []
    for name in command_names:
        if name in IGNORED_COMMANDS:
            continue
        command = getattr(module, name)
        command_infos.append(get_command_info(command))
    return command_infos


def get_embed_by_page(ctx: InteractionContext, page: Page):
    command_infos = get_command_infos_from_module(page)
    embed_fields = []
    for command_info in command_infos:
        embed_fields.append(
            EmbedField(
                name=command_info.call_name,
                value=command_info.description,
                inline=False
            )
        )

    match page:
        case Page.TALAN_MODULE:
            name = "Talan"
            description = "The list of commands relating to the bot's economy and currency system"
        case Page.GAMES_MODULE:
            name = "Games"
            description = "The list of commands relating to the various games a user can place bets on and play"
        case Page.PROFILE_MODULE:
            name = "Profile"
            description = "The list of commands relating to a user's profile on the bot"
        case Page.MISC_MODULE:
            name = "Miscellaneous"
            description = "The list of miscellaneous commands"
        case _:
            name = "Error"
            description = "Something went wrong"

    return get_embed(ctx, name, description, embed_fields)

def get_embed(ctx: InteractionContext, name: str, description: str, embed_fields: list[EmbedField]) -> Embed:
    author = EmbedAuthor(name=ctx.bot.user.username, icon_url=ctx.bot.user.avatar_url)
    timestamp = timestamp_converter(datetime.now())
    return Embed(
        title=name,
        description=description,
        timestamp=timestamp,
        fields=embed_fields,
        author=author
    )

async def change_page(ctx: InteractionContext, msg: Message, page: Page, original_ctx: SlashContext=None):
    button_ctx = original_ctx or ctx
    if isinstance(ctx, ComponentContext):
        await ctx.edit_origin(components=[get_page_changing_action_row(button_ctx), DOCS_BUTTON], embed=get_embed_by_page(ctx, page))
    else:
        await ctx.edit(msg, embed=get_embed_by_page(ctx, page), components=[get_page_changing_action_row(ctx), DOCS_BUTTON])

async def disable_buttons(ctx: SlashContext, msg: Message) -> None:
    await sleep(60)
    await ctx.edit(msg, components=[get_page_changing_action_row(ctx, True), DOCS_BUTTON])

@slash_command(
    name="help",
    description="Prompt the bot to give you its commands with a helpful description.",
)
async def help(ctx: SlashContext):
    msg = await ctx.send(components=[get_page_changing_action_row(ctx), DOCS_BUTTON], embed=get_embed_by_page(ctx, Page.MISC_MODULE))

    # @listen(Component)
    # async def on_component(component: Component):
    #     button_info = ButtonIdInfo.from_button_id(component.ctx.custom_id)
    #     is_same_ctx = button_info.ctx_id == str(ctx.id)
    #     is_same_user = button_info.user_id == str(ctx.author.id)
    #     if not is_same_ctx or not is_same_user:
    #         await component.ctx.edit_origin()
    #         return
    #     await change_page(component.ctx, msg, Page(button_info.value), original_ctx=ctx)

    for button in get_page_changing_buttons(ctx):
        @component_callback(button.custom_id)
        async def on_component(cmp_ctx: ComponentContext):
            button_info = ButtonIdInfo.from_button_id(cmp_ctx.custom_id)
            is_same_user = cmp_ctx.author.id == ctx.author.id
            if not is_same_user:
                await cmp_ctx.edit_origin()
                return
            await change_page(cmp_ctx, msg, Page(button_info.value), original_ctx=ctx)
        ctx.bot.add_component_callback(on_component)

    create_task(disable_buttons(ctx, msg))
