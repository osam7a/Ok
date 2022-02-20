from disnake.ext.commands import Cog, command, is_owner, ExtensionNotFound, ExtensionNotLoaded
from disnake import Embed

from ..utils.utils import emb
from ..utils.eval import run_eval

class DevTools(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
    
    @command(aliases = ['e'])
    @is_owner()
    async def eval(self, ctx, *, code):
        return await ctx.reply(embed = Embed(description = await run_eval(ctx, code)))
    
    @command()
    @is_owner()
    async def reload(self, ctx, cog):
        cog=cog.lower()
        try:
            self.bot.reload_extension(f"src.cogs.{cog}")
            await emb(ctx, "Reloaded.")
        except ExtensionNotLoaded:
            self.bot.load_extension(f"src.cogs.{cog}")
            await emb(ctx, "Loaded.")
        except ExtensionNotFound:
            pass
def setup(bot):
    bot.add_cog(DevTools(bot))