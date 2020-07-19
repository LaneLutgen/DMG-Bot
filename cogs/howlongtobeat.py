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
        results = HowLongToBeat().search(message)
        if results is not None and len(results) > 0:
            best_element = max(results, key=lambda element: element.similarity)
            embed = discord.Embed(title=best_element.game_name, color=discord.Color.blue())
            embed.add_field(name="Main Story", value=best_element.gameplay_main+" Hours", inline=True)
            embed.add_field(name="Main + Extras", value=best_element.gameplay_main_extra +" Hours", inline=True)
            embed.add_field(name="Completionist", value=best_element.gameplay_completionist +" Hours", inline=True)
            embed.add_field(name="Get more info about this game", value=best_element.game_web_link, inline=False)
            await ctx.trigger_typing()
            msg = await ctx.send(embed=embed)
        else:
            await ctx.send("No results found, please try redefining your search")


def setup(bot):
    bot.add_cog(Howlongtobeat(bot))
