"""Contains class for Twitch Bot"""

import os

from dotenv import load_dotenv
from twitchio.ext import commands


class Bot(commands.Bot):
    """
    Creates a subclass of the twitchio.ext.commands.Bot class
    Initialises the bot based on .env variables
    """

    def __init__(self):
        load_dotenv()
        super().__init__(
            token=os.getenv("TWITCH_ACCESS_TOKEN"),
            prefix="!",
            initial_channels=[os.getenv("TWITCH_CHANNEL")],
        )

    async def event_ready(self):
        """Method called when the Bot has successfully connected"""
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message):
        """Method called upon any message"""
        if message.echo:
            return
        print(f"{message.author}: {message.content}")

        # handles the commands within the message (e.g. !hello)
        await self.handle_commands(message)

    @commands.command()
    async def hello(self, context: commands.Context):
        """Method called when any user types !hello"""
        await context.send(f"Hello {context.author.name}!")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
