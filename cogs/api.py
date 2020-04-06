import json
from github import Github
import traceback
from discord.ext import commands
from config import get_section
from crontab import CronTab
import asyncio
import datetime

class api(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.interval = "@hourly"

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            print("Attempting to run api task")
            self.bot.loop.create_task(self.getPins(self.interval))
        except RuntimeError:
            print("Failed to run api task")
            traceback.format_exc()

    async def getPins(self, interval):
        print("getPins Running")
        guild = self.bot.get_guild(id=int(get_section("api").get("guild")))
        channel = guild.get_channel(int(get_section("api").get("pinnedChannel")))
        await self.bot.wait_until_ready()
        cron = CronTab(interval)
        while True:
            repo = Github(get_section("api").get("gitKey")).get_repo(get_section("api").get("gitRepo"))
            obj = []
            async for msg in channel.history(limit=5000):
                if(msg.pinned):
                    tmp = {"user": str(msg.author), "message": str(msg.content).replace("\n", " ")}
                    obj.append(tmp)
            file = repo.get_contents("market.json")
            repo.update_file("market.json", str(datetime.datetime.now()), json.dumps(obj), file.sha)
            print("Updated market.json")
            await asyncio.sleep(cron.next(default_utc=True))


def setup(bot):
    bot.add_cog(api(bot))
