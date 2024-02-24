"""Main file"""

import asyncio

from db_client import MDBclient
from discord_bot import DiscordBot
from gui import GUI
from logger import Logger
from twitch_bot import TwitchBot
from youtube_bot import YoutubeBot


def bot_factory(platforms, logger=None):
    """
    Initialises all the desired bots

    Args:
        platforms: List of the bots needed (List of strings)
        logger: The logger to output messages to (Optional)
    """
    bot_map = {
        "Twitch": TwitchBot,
        "Discord": DiscordBot,
        "Youtube": YoutubeBot,
    }
    bots = []
    for platform in platforms:
        if platform not in bot_map:
            raise ValueError("Unsupported Platform")
        bot = bot_map[platform](logger)
        bots += [bot]

    return bots


def main():
    """
    Main execution. Creates required bots and runs them asynchronously
    """
    db = MDBclient()
    gui = GUI()
    logger = Logger(db=db)
    platforms = ["Twitch", "Discord", "Youtube"]
    bots = bot_factory(platforms, logger)

    loop = asyncio.get_event_loop()
    for bot in bots:
        loop.create_task(bot.start())
    loop.run_forever()


if __name__ == "__main__":
    main()
