import aiohttp
from discord.ext import commands
from collections import deque
from config import get_section


class GoogleImageSearch(commands.Cog):
    """Allows you to search google images for a term. Also has a function to remove the last image, if it's not what you wanted."""
    
    def __init__(self, bot):
        self.bot = bot
        self.last_images = deque(maxlen=10)
        self.cse_api_key = get_section("show_image").get("cse_api_key")
        self.cse_cx = get_section("show_image").get("cse_cx")

        if not self.cse_api_key:
            raise Exception("Key 'cse_api_key' not found or not set.")

        if not self.cse_cx:
            raise Exception("Key 'cse_cx' not found or not set.")

    @commands.command(aliases=["rmimage","rm"])
    async def snip(self, ctx):
        """
        Deletes the most recent image. The last five images can be deleted.
        """
        if len(self.last_images) > 0:
            last_image = self.last_images.pop()
            await last_image.edit(content="[SNIP]", embed=None)


    @commands.command(aliases=["image"])
    @commands.cooldown(3, 60, commands.BucketType.user)
    async def show(self, ctx, *, arg: str):
        """
        Searches google images and shows the first image found. Safe search is on.
        """
        async with ctx.channel.typing():
            image_search = await self.google_image_search(arg)

            if image_search is not None:
                if "items" in image_search:
                    image_url = image_search["items"][0]["link"]
                    self.last_images.append(await ctx.send(image_url))
                    return None  # Exit

            await ctx.send("%s, I'm sorry. I couldn't find any images for that search.")

    @commands.command(aliases=["simage", "spoilerimage"])
    @commands.cooldown(3, 60, commands.BucketType.user)
    async def spoiler(self, ctx, *, arg: str):
        """
        Searches google images and shows the first image found. Safe search is on. Spoiler.
        """
        async with ctx.channel.typing():
            image_search = await self.google_image_search(arg)

            if image_search is not None:
                if "items" in image_search:
                    image_url = image_search["items"][0]["link"]
                    self.last_images.append(await ctx.send('||'+image_url+'||'))
                    return None  # Exit

            await ctx.send("%s, I'm sorry. I couldn't find any images for that search.")

    @show.error
    async def handle_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please tell me what to search for.', delete_after=5)
        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send('Sorry, the command is on cooldown for you right now. Try again in 60 seconds.')

    async def google_image_search(self, query):
        url = "https://www.googleapis.com/customsearch/v1"

        payload = {"q": query, "num": 1, "start": 1, "safe": "active", "searchType": "image", "key": self.cse_api_key, "cx": self.cse_cx}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as r:
                if r.status == 200:
                    js = await r.json()
                    return js
                else:
                    return None


def setup(bot):
    bot.add_cog(GoogleImageSearch(bot))
