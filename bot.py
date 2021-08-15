import argparse
import logging
import os
import platform
import sys
from configparser import ConfigParser
from pathlib import Path

from aiohttp.client_exceptions import ClientConnectorError

from core import logger, client, help

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="enable debug mode for the bot", action="store_true")
    parser.add_argument("-v", "--verbose", help="set all external logger to debug level instead of warning", action="store_true")
    parser.add_argument("-lf", "--logfile", help="output the logging information into \".log\" file instead of sys.stdout", action="store_true")

    args = parser.parse_args()

    if args.logfile:
        Path("./log").mkdir(parents=True, exist_ok=True)
        handler = logger.DailyRotatingFileHandler(basedir="./log")
    else:
        handler = logging.StreamHandler(sys.stdout)
        
    logging.basicConfig(format="[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        handlers=[handler])

    if args.verbose:
        external_level = logging.DEBUG
    else:
        external_level = logging.WARNING

    if args.debug:
        local_level = logging.DEBUG
    else:
        local_level = logging.INFO

    logging.getLogger("").setLevel(external_level)
    logging.getLogger("Azerty").setLevel(local_level)
    log = logging.getLogger("Azerty")

    cfg = ConfigParser()
    if not cfg.read("bot.ini"):
        log.error("configuration file corrupted or missing")
        sys.exit(1)

    bot = client.Bot(helpcommand=help.Help(), args=args, logger=log)
    bot.load_extension("core.commands")

    try:
        bot.run(cfg["config"]["token"])
    except ClientConnectorError:
        log.error("unable to connect to discord")
        sys.exit(1)
