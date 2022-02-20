from disnake import Member
from disnake.ext.commands import Cog, command, is_owner

from ..utils.db import EconomyDatabase

class Economy(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot 

    @command()
    async def openaccount(self, ctx):
        async with EconomyDatabase() as db:
            mem = await db.getUser(ctx.author)
            res = await mem.openAccount()
            if res:
                await ctx.send(f"Opened account, balance: {await mem.getBalance()}")
            else:
                await ctx.send("Account already exists.")
    
    @command(aliases = ['balance', 'wallet'])
    async def bal(self, ctx, member: Member = None):
        member = member or ctx.author
        async with EconomyDatabase() as db:
            mem = await db.getUser(member)
            if not mem.inDatabase:
                await mem.openAccount()
            await ctx.send(f"**Balance**: {await mem.getBalance()}")

    @command()
    @is_owner()
    async def setBal(self, ctx, user: Member, bal):
        async with EconomyDatabase() as db:
            mem = await db.getUser(user)
            if not mem.inDatabase:
                await mem.openAccount()
            await mem.setBalance(bal)
            await ctx.send(f"NEW BALANCE: {await mem.getBalance()}")

def setup(bot):
    bot.add_cog(Economy(bot))