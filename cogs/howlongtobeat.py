import discord
import howlongtobeatpy
from discord.ext import commands
from howlongtobeatpy import HowLongToBeat


class Howlongtobeat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["howlongtobeat"])
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def hltb(self, ctx, *, message: str):
        results = await HowLongToBeat().search(message)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)
            print(best_element)
        else:
            await ctx.send("No results found, please try redefining your search")


def setup(bot):
    bot.add_cog(HowLongToBeat(bot))