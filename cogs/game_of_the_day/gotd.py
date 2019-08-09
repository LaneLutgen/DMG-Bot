from discord import Game
from discord.ext import commands
import traceback
import asyncio
from crontab import CronTab
import json
import os
import random


class Gotd(commands.Cog):
    """Sets the bot's current game activity to a random game from a json file."""

    def __init__(self, bot):
        self.bot = bot
        self.interval = "@daily"

        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(os.path.join(dir_path, "./gb_games.json"), "r")
        try:
            self.game_list = json.load(f)
        except FileNotFoundError:
            print("Could not find gb_games.json. Did you run get_games.py?")
        finally:
            f.close()

    async def on_ready(self):
        await self.bot.change_presence(activity=Game(name=random.choice(self.game_list)))

        try:
            print("Scheduling random game status changer.")
            self.bot.loop.create_task(self.PlayRandomGame(self.interval))
        except RuntimeError:
            print('Could not schedule random now playing game change.')
            traceback.format_exc()

    async def PlayRandomGame(self, interval):
        await self.bot.wait_until_ready()
        cron = CronTab(interval)
        while True:
            await asyncio.sleep(cron.next(default_utc=True))
            await self.bot.change_presence(activity=Game(name=random.choice(self.game_list)))


def setup(bot):
    bot.add_cog(Gotd(bot))
