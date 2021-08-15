import fnmatch
import logging
import os
import sys
import time
import traceback
from configparser import ConfigParser
from pathlib import Path

import discord
from discord.ext import commands

from core.help import Help

cfg = ConfigParser()
if not cfg.read("bot.ini"):
    logging.getLogger("Azerty").error("configuration file corrupted or missing")
    sys.exit(1)
cfg = cfg["config"]


class Bot(commands.Bot):

    def __init__(self, helpcommand, args, logger):

        try:
            owner_ids = set(map(int, cfg["owner_ID"].split(", ")))
        except ValueError:
            owner_ids = None

        if cfg.getboolean("mention"):
            prefix = commands.when_mentioned_or(*cfg["prefix"].split(", "))
        else:
            prefix = cfg["prefix"].split(", ")

        super().__init__(command_prefix=prefix, help_command=helpcommand, owner_ids=owner_ids)

        self.log = logger
        self.args = args

    async def on_ready(self):
        """
        Called when the client is done preparing the data received from Discord.
        Usually after login is successful and the Client.guilds and co. are filled up.
        https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
        """
        time_start_bot = time.perf_counter()
        self.log.info("bot started")
        try:
            await self.user.edit(username=cfg["name"])
        except discord.errors.HTTPException:
            # blank or invalid name
            # expected behavior as specified in the ini file
            pass

        Path("./modules").mkdir(parents=True, exist_ok=True)
        for i in fnmatch.filter(os.listdir("./modules"), "*.py"):
            time_start_module = time.perf_counter()
            i = i[:-3]
            try:
                self.load_extension(f"modules.{i}")
            except Exception as e:
                self.log.warning(f"module {i} failed to load", e)
                self.log.error(traceback.format_exc())
                continue
            self.log.info(f"module {i.ljust(15)}loaded in {time.perf_counter() - time_start_module:.4f} s")
        self.log.info(f"done: total {time.perf_counter() - time_start_bot:.4f} s")

    async def on_command_error(self, ctx, error):
        if self.args.debug:
            self.log.error(error, exc_info=True)
            raise
        elif isinstance(error, commands.errors.CommandNotFound):
            pass
        elif isinstance(error, (commands.errors.NotOwner, commands.errors.MissingPermissions)):
            user = ctx.message.author
            self.log.warning(f"{user.name}#{user.discriminator} tried to use {ctx.command.name} command.")
        elif isinstance(error, commands.UserInputError):
            self.help_command.context = ctx  # in that case self.help_command.context is None. this prevent Help.get_destination() to fail
            await self.help_command.command_callback(ctx, command=str(ctx.command))
        #add command cooldownerror
        else:
            self.log.exception(error, exc_info=True)
            raise error
