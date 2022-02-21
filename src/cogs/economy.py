import random
from disnake import Member, Color, Embed
from disnake.ext.commands import Cog, command, is_owner, cooldown, BucketType

from ..utils.db import EconomyDatabase

class Economy(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot 
        self.emojis = {e.name: str(e) for e in self.bot.emojis}
        self.emoji = self.emojis['Discash']
        self.coin = lambda am: f"{self.emoji}{am}"
 
    @command()
    async def openaccount(self, ctx):
        async with EconomyDatabase() as db:
            mem = await db.getUser(ctx.author)
            res = await mem.openAccount()
            if res:
                await ctx.send(f"Opened account, balance: {self.coin(await mem.getBalance())}")
            else:
                await ctx.send("Account already exists.")
    
    @command()
    async def lb(self, ctx):
        async with EconomyDatabase() as db:
            users = await db.EconomyLeaderboard()
            print(users)
            result = ""
            for i in users:
                print(i.id)
                print(await i.getBalance())
                user = self.bot.get_user(i.id[0])
                result += f"**{user.name}#{user.discriminator}** {self.coin(await i.getBalance())}"
            await ctx.send(
                Embed(
                    title = f"Leaderboard for economy across Ok Bot",
                    description = result
                )
            )

    @command(aliases = ['balance', 'wallet'])
    async def bal(self, ctx, member: Member = None):
        member = member or ctx.author
        async with EconomyDatabase() as db:
            mem = await db.getUser(member)
            if not mem.inDatabase:
                await mem.openAccount()
            await ctx.send(f"**Balance**: {self.coin(await mem.getBalance())}")

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
    @cooldown(1, 60*10, BucketType.user)
    async def crime(self, ctx):
        async with EconomyDatabase() as db:
            mem = await db.getUser(ctx.author)
            if not mem.inDatabase:
                await mem.openAccount()
            smallAmountLoss = open("src/assets/economyStatements/smallAmountLoss.txt", "r").readlines()
            smallAmountWin = open("src/assets/economyStatements/smallAmountWin.txt", "r").readlines()
            decentAmountWin = open("src/assets/economyStatements/decentAmountWin.txt", "r").readlines()
            _ = {
                "SmallAmount": {
                    "win": {
                        "statements": smallAmountWin,
                        "gain": random.randint(100, 500)
                    },
                    "loss": {
                        "statements": smallAmountLoss,
                        "gain": random.randint(100, 500)
                    }
                }, 
                "DecentAmount": {
                    "win": {
                        "statements": decentAmountWin,
                        "gain": random.randint(500, 2000)
                    },
                    "loss": {
                        "statements": ['lost decentamount'],
                        "gain": random.randint(500, 2000)
                    }
                },
                "BigAmount": {
                    "win": {
                        "statements": ['won bigamount'],
                        "gain": random.randint(2000, 7500)
                    },
                    "loss": {
                        "statements": ['lost bigamount'],
                        "gain": random.randint(2000, 4500)
                    }
                }
            }
            
            chance = random.randint(0, 100)
            if chance < 20:
                size = "BigAmount"
            elif chance < 40:
                size = "DecentAmount"
            elif chance < 100:
                size = "SmallAmount"
            
            
            strWinOrLoss = 'win' if random.randint(0, 100) < 40 else 'loss'
            gainAndStatements = _[size][strWinOrLoss]
            gain = gainAndStatements['gain']
            statement = random.choice(gainAndStatements['statements'])
            if strWinOrLoss == "loss":
                if await mem.getBalance() - gain < 0:
                    gain = await mem.getBalance()
                await mem.setBalance(await mem.getBalance() - gain)
            else:
                await mem.setBalance(await mem.getBalance() + gain)
            await ctx.send(embed = Embed(
                description = statement + f" you {'gained' if strWinOrLoss == 'win' else 'lost'} {self.coin(gain)}",
                color = Color.green() if strWinOrLoss == "win" else Color.red()
            ))


            

            

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