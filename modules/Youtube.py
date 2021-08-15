import discord
from discord.ext import commands

class Youtube(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Youtube(bot))
