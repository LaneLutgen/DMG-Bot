import aiohttp
import discord

from config import get_section
from discord.ext import commands

class Pricechecker(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.api_token = get_section("pricechecker").get("api_token")
        if not self.api_token: raise Exception("No API Token Specified.")

    @commands.command(aliases=["pc", "price"])
    async def pricecheck(self, ctx, *, message: str):
        getresult = await self.getData(message)
        if getresult["status"] == "success":
            if not getresult["products"]: await ctx.send("No results found, please try redefining your search.")
            else:
                embed = discord.Embed(title=getresult["products"][0]["product-name"], color=discord.Color.teal())
                embed.add_field(name="Console", value=getresult["products"][0]["console-name"], inline=False)
                if getresult["products"][0]["loose-price"]/100 != 0.0: embed.add_field(name="Loose Price:", value="$"+str(getresult["products"][0]["loose-price"]/100), inline=True)
                if getresult["products"][0]["cib-price"]/100 != 0.0: embed.add_field(name="CIB Price:", value="$"+str(getresult["products"][0]["cib-price"]/100), inline=True)
                if getresult["products"][0]["new-price"]/100 != 0.0: embed.add_field(name="NEW Price:", value="$"+str(getresult["products"][0]["new-price"]/100), inline=True)
                embed.add_field(name="Get more info about this game", value="https://www.pricecharting.com/game/" + str(getresult["products"][0]["id"]), inline=False)
                await ctx.channel.trigger_typing()
                await ctx.send(embed=embed)
        else: await ctx.send("Something went wrong, please try again")

    async def getData(self, game):
        url = "https://www.pricecharting.com/api/products"
        payload = {"t": self.api_token, "q": game}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=payload) as r:
                if r.status == 200:
                    js = await r.json()
                    return js
                else: return None
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument): await ctx.send("Please specify a game you want to search for")

def setup(bot):
    bot.add_cog(Pricechecker(bot))
