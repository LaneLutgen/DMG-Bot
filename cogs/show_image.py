import discord
import aiohttp
from discord.ext import commands
from collections import deque

import config


class GoogleImageSearch(object):
    def __init__(self, bot):
        self.bot = bot
        self.last_images = deque(maxlen=10)

    @commands.command()
    async def snip(self, ctx):
        """
        Deletes the most recent image. The last five images can be deleted.
        """
        if len(self.last_images) > 0:
            last_image = self.last_images.pop()
            await last_image.edit(content="[SNIP]", embed=None)


    @commands.command()
    async def show(self, ctx, *, arg: str):
        """
        Searches google images and shows the first image found. Safe search is on.
        """
        async with ctx.channel.typing():
            image_search = await self.google_image_search(arg)

            if image_search is not None:
                if "items" in image_search:
                    image_url = image_search["items"][0]["link"]
                    self.last_images.append(await ctx.send("%s: " % ctx.author.mention + image_url))
                    return None  # Exit

            await ctx.send("%s, I'm sorry. I couldn't find any images for that search." % ctx.author.mention)

    @show.error
    async def handle_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me what to search for.', delete_after=5)

    async def google_image_search(self, query):
        url = "https://www.googleapis.com/customsearch/v1"

        payload = {"q": query, "num": 1, "start": 1, "safe": "active", "searchType": "image", "key": config.CSE_API_KEY, "cx": config.CSE_CX}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as r:
                if r.status == 200:
                    js = await r.json()
                    return js
                else:
                    return None


def setup(bot):
    bot.add_cog(GoogleImageSearch(bot))