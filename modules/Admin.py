import discord
from discord.ext import commands


class Admin(commands.Cog):
    """Admin function. reserved to the member who have permissions"""

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            pass
        else:
            raise error

    # @commands.command()
    # async def clear(self, ctx, qte: int):
    #     """
    #     clear an amount of message
    #     messages older than 14 days will not be removed
    #     """
    #     if qte <= 0:
    #         await ctx.send(embed=discord.Embed(title=":x: select a valid amount of message to delete", color=0xff0000))
    #         return
    #     if qte > 100:
    #         await ctx.send(embed=discord.Embed(title=":x: cannot delete more than 100 messages", color=0xff0000))
    #         return

    # @commands.command()
    # async def mute(self, ctx, user: discord.Member, delay: int = None):
    #     """"mute an user (optionnal delay)"""
    #     pass

    # @commands.command()
    # async def unmute(self, ctx, user: discord.Member):
    #     pass

    @commands.command()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member, *, reason: str = None):
        if user == ctx.message.author:
            await ctx.send(embed=discord.Embed(title=":warning: you cannot kick yourself!", color=0xff0000))
            return
        if reason is None: reason = "no reason given"
        await ctx.send(
            embed=discord.Embed(
                title=f":thong_sandal: user {user.name} has been kicked by {ctx.message.author.name}",
                description=f"reason\n```{reason}```"))
        await user.send(
            embed=discord.Embed(
                description=f"you have been kicked from {ctx.guild.name} by {ctx.message.author.name} for reason: ```{reason}```"))
        await self.bot.kick(user, reason=reason)

    @commands.command()
    @commands.has_guild_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason: str = None):
        if user == ctx.message.author:
            await ctx.send(embed=discord.Embed(title=":warning: you cannot ban yourself!", color=0xff0000))
            return
        if reason is None: reason = "no reason given"
        await ctx.send(
            embed=discord.Embed(
                title=f":hammer: user {user.name} has been banned by {ctx.message.author.name}",
                description=f"reason\n```{reason}```"))
        await user.send(
            embed=discord.Embed(
                description=f"you have been banned from {ctx.guild.name} by {ctx.message.author.name} for reason: ```{reason}```"))
        await self.bot.ban(user, reason=reason)


def setup(bot):
    bot.add_cog(Admin(bot))
