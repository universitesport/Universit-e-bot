import discord
import random
from discord.ext import commands

class EasterEggs(commands.Cog, hidden=True):

    def __init__(self, bot):
        self.bot = bot

    @commands.is_owner()
    @commands.command(hidden=True)
    async def echo(self, ctx, *, msg):
        await ctx.send(msg)

    @commands.command(hidden=True)
    async def sardoche(self, ctx):
        await ctx.send(random.choice(
            ["Mais c'était sûr en fait !",
             "Il est mort, le noir est mort",
             "POURQUOI ? POURQUOI ? POURQUOI ?"]))

def setup(bot):
    bot.add_cog(EasterEggs(bot))
