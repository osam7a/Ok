from disnake.ext.commands import Cog
from disnake import Embed

class Listeners(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        
def setup(bot):
    bot.add_cog(Listeners(bot))