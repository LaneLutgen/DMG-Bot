from discord.ext import commands


class imgurAlbumHandler(commands.Cog):
    """Keeps an eye on imgur album links and informs about them"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """Keeps an eye on imgur album links and informs about them"""
        if any([keyword in ctx.content.upper() for keyword in ('IMGUR.COM/A/', 'IMGUR.COM/GALLERY/')]):
            await ctx.channel.trigger_typing()
            await ctx.channel.send("The message posted by " + ctx.author.mention + " contains an imgur album link, it may have more than one image")
            
def setup(bot):
    bot.add_cog(imgurAlbumHandler(bot))
