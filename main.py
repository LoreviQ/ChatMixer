"""Main file"""

import asyncio

from db_client import MDBclient
from discord_bot import DiscordBot
from gui import GUI
from logger import Logger
from twitch_bot import TwitchBot
from youtube_bot import YoutubeBot

if __name__ == "__main__":
    db = MDBclient()
    gui = GUI()
    logger = Logger(db=db)
    discordBot = DiscordBot(logger)
    twitchBot = TwitchBot(logger)
    youtubeBot = YoutubeBot(logger)

    loop = asyncio.get_event_loop()
    loop.create_task(discordBot.start(discordBot.token))
    loop.create_task(twitchBot.start())
    loop.create_task(youtubeBot.start())
    loop.run_forever()
