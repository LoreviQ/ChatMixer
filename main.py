"""Main file"""

from db_client import MDBclient
from logger import Logger
from twitch_bot import TwitchBot

if __name__ == "__main__":
    db = MDBclient()
    logger = Logger(db)
    bot = TwitchBot(logger)
    bot.run()
