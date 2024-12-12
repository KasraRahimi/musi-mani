from dataclasses import dataclass
import commands
from interactions import slash_command, Button, ButtonStyle, SlashContext, SlashCommand, ActionRow

from commands.utils import get_button_id

DOCS_BUTTON = ActionRow(Button(
    style=ButtonStyle.LINK,
    url="https://kawa-4.gitbook.io/musi-mani",
    label="Documentation",
))

MISC_MODULE = 'misc'
TALAN_MODULE = 'talan'
PROFILE_MODULE = 'user_profile'
GAMES_MODULE = 'games'

def get_page_changing_action_row(ctx: SlashContext) -> ActionRow:
    return ActionRow(
        Button(
            style=ButtonStyle.SECONDARY,
            label="Misc",
            custom_id=get_button_id(MISC_MODULE, ctx),
            emoji="🔮"
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Talan",
            custom_id=get_button_id(TALAN_MODULE, ctx),
            emoji="🪙",
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Profile",
            custom_id=get_button_id(PROFILE_MODULE, ctx),
            emoji="ℹ️"
        ),
        Button(
            style=ButtonStyle.SECONDARY,
            label="Games",
            custom_id=get_button_id(GAMES_MODULE, ctx),
            emoji="🎲"
        )
    )

@dataclass
class CommandInfo:
    name: str
    description: str

    @property
    def call_name(self) -> str:
        return f"/{self.name}"

@slash_command(
    name="help",
    description="send a help message to help explain how to use the bot",
)
async def help(ctx: SlashContext):
    content = (
        "Hi, :wave:",
        "I'm ilo musi, I'm a discord gambling bot. I offer a variety of casino games you can bet talan on. I will have a more useful help message soon. For now, refer to my documentation with the link below."
    )
    content = "\n".join(content)
    await ctx.send(content, components=DOCS_BUTTON)

def get_command_info(cmd: SlashCommand) -> CommandInfo:
    if cmd.is_subcommand:
        name = f"{cmd.name} {cmd.sub_cmd_name}"
        description = cmd.sub_cmd_description
    else:
        name = cmd.name
        description = cmd.description
    return CommandInfo(name, description)

def get_command_infos_from_module(module_name: str) -> list[CommandInfo]:
    module = getattr(commands, module_name)
    command_names = module.__all__
    command_infos = []
    for name in command_names:
        command = getattr(module, name)
        command_infos.append(get_command_info(command))
    return command_infos

if __name__ == "__main__":
    name = 'talan'
    command_infos = get_command_infos_from_module(name)
    for info in command_infos:
        print(info.name)
        print(info.call_name)
        print(info.description)
        print()