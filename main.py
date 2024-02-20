"""Main file"""

import asyncio

from db_client import MDBclient
from discord_bot import DiscordBot
from gui import GUI
from logger import Logger
from twitch_bot import TwitchBot

if __name__ == "__main__":
    db = MDBclient()
    # gui = GUI()
    logger = Logger(db=db)
    discordBot = DiscordBot(logger)
    twitchBot = TwitchBot(logger)

    loop = asyncio.get_event_loop()
    loop.create_task(discordBot.start(discordBot.token))
    loop.create_task(twitchBot.start())
    loop.run_forever()
