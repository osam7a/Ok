from typing import Union
from disnake import Member, User
from disnake.ext.commands import Cog, command, has_permissions
from datetime import datetime
from time_str import convert
from ..utils.utils import emb
from disnake.utils import sleep_until

class Mod(Cog):
    def __init__(self, bot) -> None:
        self.bot = bot 
    
    @command(aliases = ['timeout', 'silence', 'shut'])
    @has_permissions(manage_messages = True)
    async def mute(self, ctx, member: Union[Member, User], duration = None, *, reason = "No reason provided."):
        if duration == None:
            duration = convert("300 years")
            dur = "Permanently"
        if isinstance(member, User):
            member = ctx.guild.get_member(member)
        else:
            dur = duration
            duration = convert(duration)
        now = datetime.utcnow()
        diff = now + duration
        await member.timeout(until = diff, reason = reason)
        await emb(ctx, f"Muted {member.mention} for {dur}, reason: {reason}")
        try:
            await emb(member, f"You were muted in {ctx.guild.name} for {dur}, reason: {reason}", user = member)
        except: pass
    
    @command()
    @has_permissions(manage_messages = True)
    async def unmute(self, ctx, member: Union[Member, User], *, reason = "No reason provided"):
        if isinstance(member, User):
            member = ctx.guild.get_member(member)
        await member.timeout(until = None, reason = reason)
        await emb(ctx, f"Unmuted {member.mention}, reason: {reason}")
        try:
            await emb(member, f"You were unmuted in {ctx.guild.name}, reason: {reason}", user = member)
        except: pass

    @command()
    @has_permissions(ban_members = True)
    async def ban(self, ctx, member: Union[Member, User], duration = None, *, reason = "No reason provided."):
        if duration == None:
            duration = convert("300 years")
            dur = "Permanently"
        else:
            dur = duration
            duration = convert(duration)
        now = datetime.utcnow()
        diff = now + duration

        try:
            await emb(ctx, f"Banned {member.mention} for {dur}, reason: {reason}")
        except: pass
        try:
            await emb(member, f"You were banned from {ctx.guild.name} for {dur}, reason: {reason}", user = member)
        except: pass
        await member.ban(reason = reason)
        await sleep_until(diff)
        await member.unban(reason = reason)
        try:
            await emb(member, f"You are unbanned from {ctx.guild.name}!, join now using: {await ctx.channel.create_invite().url}", user = member)
        except: pass
        
def setup(bot):
    bot.add_cog(Mod(bot))