from typing import *

import discord
from discord.ext import commands

class Tournament(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tournament(self, ctx):
        """
        list all current tournament
        """
        if ctx.invoked_subcommand is None:
            pass  # list all tournaments in progress

    @commands.is_owner()
    @tournament.command(aliases=["new"])
    async def create(self, ctx, name: str):
        """
        create a new tournament with the specified parameters
        """
        pass

    @commands.is_owner()
    @tournament.command()
    async def delete(self, ctx, id: Union[int, str], *, reason: Optional[str]=None):
        """
        delete the specified tournament
        """
        pass

    @commands.is_owner()
    @tournament.command()
    async def modify(self, ctx, id: Union[int, str]):
        """
        edit the specified tournament
        """
        pass

    @tournament.command()
    async def register(self, ctx, id: Union[int, str]):
        """
        register yourself to the specified tournament
        exemple: $register ULLAN2020 csgo, rocket_league
        """
        pass

    @tournament.command()
    async def unregister(self, ctx, id: Union[int, str]):
        """
        unregister you from a tournament or a specific game
        exemple: $unregister ULLAN2020
        or: $unregister ULLAN2020 csgo
        """
        pass

    @tournament.command(aliases=["check-in"])
    async def checkin(self, ctx, id: Union[int, str]):
        """
        to confirm you presence to a tournament (from 2 days up to 1 hour before it start)
        """
        pass

    @tournament.command(aliases=["info"])
    async def infos(self, ctx, id: Optional[Union[int, str]]):
        """
        all details about a specific tournament
        """
        pass

def setup(bot):
    bot.add_cog(Tournament(bot))
