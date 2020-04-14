from discord.ext import commands

class chocklocator(commands.Cog):
    """Keeps an eye on imgur album links and informs about them"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 360, commands.BucketType.guild)
    async def locatechock(self, ctx):
        await ctx.channel.trigger_typing()
        await ctx.channel.send("I've located Chock, <@!145329600963018753>")


def setup(bot):
    bot.add_cog(chocklocator(bot))
