from disnake.ext import commands
import disnake

class HelpCommand(commands.MinimalHelpCommand):
  def add_bot_commands_formatting(self, commands, heading):
        if commands:
            # U+2002 Middle Dot
            joined = "\u2002".join(c.name for c in commands)
            self.paginator.add_line(f"__**{heading}**__")
            self.paginator.add_line(joined)

  def get_command_signature(self, command):
        parent = command.parent
        entries = []
        while parent is not None:
            if not parent.signature or parent.invoke_without_command:
                entries.append(parent.name)
            else:
                entries.append(parent.name + " " + parent.signature)
            parent = parent.parent
        parent_sig = " ".join(reversed(entries))

        if len(command.aliases) > 0:
            aliases = "|".join(command.aliases)
            fmt = f"[{command.name}|{aliases}]"
            if parent_sig:
                fmt = parent_sig + " " + fmt
            alias = fmt
        else:
            alias = command.name if not parent_sig else parent_sig + " " + command.name

        return f"```yaml\nUsage: {self.context.clean_prefix}{alias} {command.signature}\n```"

  def get_opening_note(self):
        command_name = self.invoked_with
        return (
            f"```\nUse {self.context.clean_prefix}{command_name} [command] for more info on a command.\n"
            f"You can also use {self.context.clean_prefix}{command_name} [category] for more info on a category.\n```"
        )

  async def send_pages(self):
    destination = self.get_destination()
    for page in self.paginator.pages:
        await destination.send(embed = disnake.Embed(description = page, color = self.context.bot.color).set_footer(text = f"Use {self.context.prefix}help <command/category> to get info about a command or a category"))