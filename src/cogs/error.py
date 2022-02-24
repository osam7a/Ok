import traceback
import random

# Exceptions Imports
from disnake.ext.commands import (
    Bot,
    Cog,
    BotMissingPermissions,
    MissingPermissions,
    MissingRole,
    DisabledCommand,
    ChannelNotFound,
    MemberNotFound,
    UserNotFound,
    TooManyArguments,
    CommandOnCooldown,
    MissingRequiredArgument,
    Context,
    PrivateMessageOnly,
    NoPrivateMessage,
)

from disnake import Embed, Color
from disnake.ext.commands.errors import CommandNotFound, RoleNotFound, NotOwner

from ..utils.utils import emb

from ..utils.logging import Log

class ErrorHandler(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.commandLog = Log("src/logs/command.log")

    @staticmethod
    def underline(text, at, for_):
        underline = (" " * at) + ("^" * for_)
        return text + "\n" + underline

    @staticmethod
    def signature_parser(cmd) -> str:
        command_signature = ""
        for arg in cmd.signature.split(" ")[: len(cmd.params) - 2]:
            if "=" in arg:
                parsed_arg = "{" + arg.split("=")[0].strip("[]<>]") + "}"
            else:
                parsed_arg = "[" + arg.strip("[]<>") + "]"
                if parsed_arg == "[]":
                    parsed_arg = ""
            command_signature += parsed_arg + " "
        return command_signature

    @staticmethod
    def perms_parser(perms: list) -> str:
        return f"`{'` , `'.join(perms).title().replace('guild','server').replace('_',' ')}`"

    @Cog.listener()
    async def on_command_error(self, ctx: Context, error: Exception):
        if isinstance(error, CommandNotFound):
            return
        elif isinstance(error, MissingRequiredArgument):
            desc = (
                f"{ctx.prefix} {ctx.command.name} {self.signature_parser(ctx.command)}"
            )
            inside = self.underline(
                desc, desc.index(f"[{error.param.name}]"), len(f"[{error.param.name}]")
            )
            desc = f"\n```ini\n{inside}\n```"
            await ctx.send(
                embed=Embed(
                    description=f"Seems like you didn't provide a required argument : `{error.param.name}`{desc}",
                    color=Color.red(),
                )
            )
        elif isinstance(error, RoleNotFound):
            await ctx.send(
                embed=Embed(
                    description=f"Unable to find a role named `{error.argument}`",
                    color=Color.red(),
                )
            )
        elif isinstance(error, CommandOnCooldown):
            if round(error.retry_after) > 60*60:
                    time = f"{round(error.retry_after / (60*60))} hours"
            elif round(error.retry_after) > 60:
                    time = f"{round(error.retry_after / 60)} minutes"
            else:
                    time = f"{round(error.retry_after)} seconds"
            cooldown_embed = Embed(
                title=random.choice(
                    [
                        "Slow down!",
                        "You're going a little too fast bud...",
                        "Hold your horses!",
                        "Noooooo!",
                        "Woah now, slow it down...",
                        "Take a breather...",
                        "NEGATORY.",
                    ]
                ),
                description=f"This command is on a cooldown! try again in {time}",
                color=Color.red(),
            )
            await ctx.send(embed=cooldown_embed)
        elif isinstance(error, MissingPermissions):
            await ctx.send(
                embed=Embed(
                    description=f"You are missing `{self.perms_parser(error.missing_permissions)}` permissions required to run the command",
                    color=Color.red(),
                ),
            )
        elif isinstance(error, BotMissingPermissions):
            await ctx.send(
                embed=Embed(
                    description=f"I am missing `{self.perms_parser(error.missing_permissions)}` permissions required to run the command",
                    color=Color.red(),
                )
            )
        elif isinstance(error, MemberNotFound):
            await ctx.send(
                embed=Embed(
                    description=f"Unable to find any member named `{error.argument}` in `{ctx.guild.name}`",
                    color=Color.red(),
                )
            )
        elif isinstance(error, UserNotFound):
            await ctx.send(
                embed=Embed(
                    description=f"Unable to find a user named `{error.argument}`",
                    color=Color.red(),
                )
            )

        elif isinstance(error, ChannelNotFound):
            await ctx.send(
                embed=Embed(
                    description=f"No channel named `{error.argument}` found",
                    color=Color.red(),
                )
            )
        elif isinstance(error, MissingRole):
            await ctx.send(
                embed=Embed(
                    description=f"You need `{error.missing_role}` role in order to use this command",
                    color=Color.red(),
                )
            )
        elif isinstance(error, NotOwner):
            await ctx.send(
                embed=Embed(
                    title="No No",
                    description=f"`{ctx.command.name}` is an owner only command , only bot owner(s) can use it",
                    color=Color.red(),
                )
            )
        elif isinstance(error, TooManyArguments):
            await ctx.send(
                embed=Embed(
                    title=f"Too many arguments provided , **Usage :** ```\nini{ctx.prefix} {ctx.command.name} {self.signature_parser(ctx.command)}\n```",
                    color=Color.red(),
                )
            )
        elif isinstance(error, DisabledCommand):
            await ctx.send(
                embed=Embed(description="This command is disabled", color=Color.red())
            )
        elif isinstance(error, PrivateMessageOnly):
            await ctx.send(
                embed=Embed(
                    description=f"`{ctx.command.name}` can be used only in DMs",
                    color=Color.red(),
                )
            )
        elif isinstance(error, NoPrivateMessage):
            await ctx.send(
                embed=Embed(
                    description=f"`{ctx.command.name}` command cannot be used in DMs",
                    color=Color.red(),
                )
            )
        else:
            self.commandLog.error(''.join(traceback.format_exception(error, error, error.__traceback__)))
            await emb(ctx, f"Whoops! Something went wrong... Please contact osam7a#1017 to check the logs and fix this!")
            print("Command ERROR, check command.log")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))