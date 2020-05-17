import json
from github import Github
import traceback
from discord.ext import commands
from config import get_section
from crontab import CronTab
import asyncio
import datetime
import base64


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

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = self.bot.get_guild(id=int(get_section("api").get("guild")))
        if message.channel == guild.get_channel(int(get_section("api").get("pinnedChannel"))):
            if any([keyword in message.content.upper() for keyword in (':BUYING:', ':SELLING:', ':WTB:', ':WTS:', ':TRADING:', ':WTT:')]):
                await message.pin()


    async def getPins(self, interval):
        print("getPins Running")
        guild = self.bot.get_guild(id=int(get_section("api").get("guild")))
        channel = guild.get_channel(int(get_section("api").get("pinnedChannel")))
        await self.bot.wait_until_ready()
        cron = CronTab(interval)
        repo = Github(get_section("api").get("gitKey")).get_repo(get_section("api").get("gitRepo"))
        obj = []
        eurl = ""
        aurl = ""
        while True:
            async for msg in channel.history(limit=5000):
                if(msg.pinned):
                    if msg.embeds:
                        eurl = []
                        eurl.clear()
                        for embed in msg.embeds:
                            eurl.append(str(embed.url))

                    if msg.attachments:
                        aurl = []
                        for attachment in msg.attachments:
                            aurl.append(str(attachment.url))

                    tmp = {"user": str(msg.author), "message": str(msg.content), "created": str(msg.created_at), "avatar_url": str(msg.author.avatar_url), "message_id": str(msg.id), "embeds": str(eurl), "attachments": aurl}
                    obj.append(tmp)
                    eurl = ""
                    aurl = ""
            file = repo.get_contents("market.json")
            encode = base64.b64encode(str(json.dumps(obj)).encode("utf-8"))
            if str(file.content).replace('\n', '') == str(encode, "utf-8"):
                print("Data is unchanged, no commit was made")
                await asyncio.sleep(cron.next(default_utc=True))
                obj.clear()
                tmp.clear()
            else:
                repo.update_file("market.json", str(datetime.datetime.now()), json.dumps(obj), file.sha)
                print("Updated market.json")
                await asyncio.sleep(cron.next(default_utc=True))
                obj.clear()
                tmp.clear()


def setup(bot):
    bot.add_cog(api(bot))
