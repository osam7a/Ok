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

    @command(aliases=['give'])
    async def pay(self, ctx, member: Member, amount: int):
        async with EconomyDatabase() as db:
            mem = await db.getUser(member)
            author = await db.getUser(ctx.author)
            if not mem.inDatabase:
                await mem.openAccount()
            elif not author.inDatabase:
                await author.openAccount()
            if await author.getBalance()-amount < 0:
                await ctx.send(f"You do not have that amount, {ctx.author.mention}")
            else:
                await mem.setBalance(await mem.getBalance() + amount)
                await author.setBalance(await author.getBalance() - amount)

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