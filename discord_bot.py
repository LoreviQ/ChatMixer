"""Contains class for Discord Bot"""

import os

import discord
from dotenv import load_dotenv


class DiscordBot(discord.Client):
    """
    Creates a subclass of the discord.Client class
    Initialises the bot based on .env variables
    """

    def __init__(self, logger=None):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.platform = "Discord"
        self.logger = logger
        self.token = os.getenv("DISCORD_TOKEN")

    async def on_ready(self):
        """Method called when the Bot has successfully connected"""
        print(f"Connected to {self.platform} as: {self.user}")

    async def on_message(self, message):
        """
        Method called upon any message, logs the message

        Args:
            message: discord message class
        """
        if message.author == self.user:
            return
        if self.logger:
            self.logger.log_message(message.author.name, self.platform, message.content)

    async def start(self):
        await super().start(self.token)


if __name__ == "__main__":
    load_dotenv()
    bot = DiscordBot()
