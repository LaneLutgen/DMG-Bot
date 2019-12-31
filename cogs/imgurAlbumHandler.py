from discord.ext import commands

class imgurAlbumHandler(commands.Cog):
    """Keeps an eye on imgur album links and informs about them"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, ctx):
        """Keeps an eye on imgur album links and informs about them"""
        if 'imgur.com/a/' in ctx.content:
            await ctx.channel.trigger_typing()
            await ctx.channel.send("The link posted by " + ctx.author.mention + " contains an imgur album link, and may have more than one image")
        if 'imgur.com/gallery/' in ctx.content:
            await ctx.channel.trigger_typing()
            await ctx.channel.send("The link posted by " + ctx.author.mention + " Contains an imgur album link, and may have more than one image")

def setup(bot):
    bot.add_cog(imgurAlbumHandler(bot))
