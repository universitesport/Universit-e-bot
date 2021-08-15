import datetime
import os
import platform
import sys
import time
import traceback

import discord
from dateutil.relativedelta import relativedelta
from discord.ext import commands
from psutil import Process


class CoreCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def module(self, ctx, action: str, name: str):
        """
        module manager command. you can load, unload or reload a module
        """
        if action not in {"reload", "load", "unload"}:
            await ctx.send(embed=discord.Embed(title=f":x: unknown action \"{action}\"", color=0xff0000))
            return
        try:
            start = time.perf_counter()
            if action == "unload":
                self.bot.unload_extension(f"modules.{name}")
            elif action == "load":
                self.bot.load_extension(f"modules.{name}")
            elif action == "reload":  # else?
                self.bot.reload_extension(f"modules.{name}")
            stop = time.perf_counter()

        except (commands.errors.ExtensionNotLoaded,
                commands.errors.ExtensionNotFound,
                commands.errors.ExtensionAlreadyLoaded) as e:
            await ctx.send(embed=discord.Embed(title=f":x: {str(e).replace('modules.', '')}", color=0xff0000))
        except Exception as e:
            await ctx.send(embed=discord.Embed(title=":x: unexpected error",
                                               description=f"{type(e)}\n```{e}```\nsee CMD output for more details",
                                               color=0xff0000))
            self.bot.log.error(f"fail to {action} module {name}: {type(e)}")
            self.bot.log.exception(e)
        else:
            await ctx.send(embed=discord.Embed(title=f":white_check_mark: module {name} {action}ed", color=0x00ff00))
            self.bot.log.info(f"module {name} {action}ed by {ctx.message.author.name}#{ctx.message.author.discriminator} in {stop-start:.4f} s")

    # @commands.command()
    # @commands.is_owner()
    # async def getlog(self, ctx, *, date: str = None):
    #     """
    #     send the log file of the specified date. if no date is provide the current logfile is sent if exist
    #     """
    #     if date is None:
    #         date = datetime.date.today().strftime("%Y-%m-%d")
    #     else:
    #         date = datetime.date(*map(int, reversed(date.split(" ")))).strftime("%Y-%m-%d")  # todo: rework this mess
    #     if not os.path.isfile(f"./log/{date}.log"):
    #         await ctx.send(embed=discord.Embed(
    #             title=f":x: no log file at this date\nbe sure to use the command like this:\n```{ctx.prefix}getlog dd mm yyyy```",
    #             color=0xff0000))
    #         return
    #     with open(f"./log/{date}.log", "rb") as file:
    #         await ctx.send(
    #             embed=discord.Embed(title=f""":floppy_disk: log file of {"/".join(reversed(date.split("-")))}""",
    #                                 color=0x2f4f4f))
    #         await ctx.send(file=discord.File(file, filename=f"{date}.log"))

    @commands.command()
    async def info(self, ctx):
        """
        display informations about the bot
        all credits for this command belong to frenshmastersword, author of the [RTFM bot](https://github.com/FrenchMasterSword "RTFM bot")
        """
        embed = discord.Embed(title=self.bot.user.name, color=0x00ff00)
        embed.add_field(name="Servers count", value=f"```{len(self.bot.guilds)}```")
        embed.add_field(name="Total member count", value=f"```{sum([guild.member_count for guild in self.bot.guilds])}```", inline=False)
        embed.add_field(name="Language", value=f"```Python {sys.version[:5]} with {platform.python_implementation()}```", inline=False)
        embed.add_field(name="Discord API version", value=f"```discord.py {discord.__version__}```", inline=False)
        embed.add_field(name="Hosting", value=f"```{platform.platform()}```", inline=False)
        delta = relativedelta(seconds=int(time.time() - Process(os.getpid()).create_time()))
        uptime = str()
        if delta.days:
            uptime += f"{int(delta.days)} d "
        if delta.hours:
            uptime += f"{int(delta.hours)} h "
        if delta.minutes:
            uptime += f"{int(delta.minutes)} m "
        if delta.seconds:
            uptime += f"{int(delta.seconds)} s"
        embed.add_field(name="Uptime", value=f"```{uptime}```", inline=False)
        embed.add_field(name="Latency", value=f"```{int(self.bot.latency * 1000)} ms```")
        embed.add_field(name="Powered by Azerty bot", value="""[base your bot on Azerty](https://github.com/desaleo/Azerty-bot "Leave a star")\n\
        [Report a bug or make a suggestion](https://github.com/desaleo/Azerty-bot/issues "Open an issue")\n""",
                        inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        """
        display the current latency of the bot
        """
        await ctx.send(f"pong!\ncurrent latency: {int(self.bot.latency*1000)} ms")

    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        """
        shutdown the bot
        """
        await ctx.message.add_reaction("\U00002705")
        self.bot.log.info(f"bot closed by {ctx.message.author.name}#{ctx.message.author.discriminator}")
        try:
            await self.bot.close()
        except RuntimeError:
            pass  # https://bugs.python.org/issue39232


def setup(bot):
    bot.add_cog(CoreCommands(bot))
