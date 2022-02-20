import traceback
from pathlib import Path
from os import listdir
import logging

from .utils.logging import Log
from .utils.HIDDEN import TOKEN

from disnake import Color
from disnake import AllowedMentions
from disnake.ext.commands import Bot, ExtensionFailed, ExtensionError

class Ok(Bot):
    def __init__(self, prefix, help):
        super().__init__(prefix, help_command=help, allowed_mentions = AllowedMentions(everyone=False, roles=False))
        self.botLog = Log("src/logs/bot.log", clear = False)
        self.cogLog = Log("src/logs/cog.log")
        self.commandLog = Log("src/logs/command.log")
        self.color = Color.blue()
        self.listenerPrefix = f"okAI "
        self.cwd = cwd = Path(__file__).parents[0]

    def run(self):
        @self.after_invoke
        async def afterInvoke(ctx):
            self.commandLog.info(f"{ctx.command.name} Was successfully executed by {ctx.author}")

        try:
            ext = []
            for i in listdir(str(self.cwd) + "/cogs"):
                if i.endswith(".py"):
                    ext.append(f"src.cogs.{i[:-3]}")
            
            for i in ext: 
                try:
                  self.load_extension(i)
                  self.cogLog.info(f"Cog \"{i}\" was loaded.")
                except ExtensionFailed or ExtensionError as error: 
                    logging.error(f"Cog {i} failed, Check cog.log")
                    return self.cogLog.error(''.join(traceback.format_exception(error, error, error.__traceback__)))
        except Exception as error:
            self.cogLog.error(''.join(traceback.format_exception(error, error, error.__traceback__)))
            logging.error("Cogs failed, check cog.log")
        
        self.botLog.info(f"Bot is running... Cog Count: {len(self.cogs)}, Command Count: {len(self.commands)}")
        super().run(TOKEN)
