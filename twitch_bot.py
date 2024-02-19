"""Contains class for Twitch Bot"""

import os

from twitchio.ext import commands


class Bot(commands.Bot):
    """
    Creates a subclass of the twitchio.ext.commands.Bot class
    Initialises the bot based on .env variables
    """

    def __init__(self):
        super().__init__(
            token=os.environ["ACCESS_TOKEN"],
            prefix="!",
            initial_channels=[os.environ["CHANNEL"]],
        )

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    @commands.command()
    async def hello(self, context: commands.Context):
        """Command triggered when any user types !hello"""
        await context.send(f"Hello {context.author.name}!")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
