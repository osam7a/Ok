from dataclasses import dataclass
import re
from disnake import File
import matplotlib.pyplot as plt
from math import cos, sin, sqrt
from typing import Union
from disnake.ext.commands import Cog, command
from numpy import array, linspace
from ..utils.utils import emb
import simpleeval

class Math(Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @command()
    async def plot(self, ctx, equationType, equation):
        if equationType == "slope-intercept":
            await ctx.send(f"**!** Still In Development **!**\nThis command is still under development, it might not work properly")
            mtch = re.match(f"y=(?P<slope>.+)x\+(?P<yintercept>.+)", equation, flags = re.IGNORECASE)
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            x = linspace(-5,5,100)
            ax.spines['left'].set_position('center')
            ax.spines['bottom'].set_position('center')
            ax.spines['right'].set_color('none')
            ax.spines['top'].set_color('none')
            ax.xaxis.set_ticks_position('bottom')
            ax.yaxis.set_ticks_position('left')
            plt.plot(x, float(mtch.groupdict()['slope'])*x+float(mtch.groupdict()['yintercept']), '-r', label=equation)
            plt.legend(loc='upper left')
            plt.savefig("src/assets/plot.png")
            await ctx.send(file = File("src/assets/plot.png"))



    @command()
    async def sqrt(self, ctx, number: Union[float, int]):
        return await emb(ctx, f"```\n{sqrt(number)}\n```")
    
    @command()
    async def cos(self, ctx, number: Union[float, int]):
        return await emb(ctx, f"```\n{cos(number)}\n```")

    @command()
    async def sin(self, ctx, number: Union[float, int]):
        return await emb(ctx, f"```\n{sin(number)}\n```")

    @command()
    async def calculate(self, ctx, equation):
        result = simpleeval.simple_eval(equation)
        if result > 2000:
            result = result[:-1900]
        return await emb(ctx, f"```\n{result}\n```")
        
    @command()
    async def round(self, ctx, number: float):
        return await emb(ctx, f"```\n{round(number)}\n```")

def setup(bot):
    bot.add_cog(Math(bot))