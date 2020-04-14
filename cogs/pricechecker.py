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
    @commands.cooldown(3, 60, commands.BucketType.user)
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
                embed.add_field(name="Search Query", value=message, inline=True)
                embed.add_field(name="Result", value="1/" + str(len(getresult["products"])), inline=True)
                embed.add_field(name="Get more info about this game", value="https://www.pricecharting.com/game/" + str(getresult["products"][0]["id"]), inline=False)
                await ctx.trigger_typing()
                msg = await ctx.send(embed=embed)
                await msg.add_reaction(emoji = "\u2B05")
                await msg.add_reaction(emoji = "\u27A1")
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

    async def changeCheckPage(self, search: str, channel: discord.TextChannel, message: discord.Message, author_id: int = "", page: int = 0):
        getresult = await self.getData(search)
        if getresult["status"] == "success":
            if not getresult["products"]: await channel.send("No results found, please try redefining your search.")
            else:
                if page <= int(len(getresult["products"])-1):
                    embed = discord.Embed(title=getresult["products"][page]["product-name"], color=discord.Color.teal())
                    embed.add_field(name="Console", value=getresult["products"][page]["console-name"], inline=False)
                    if getresult["products"][page]["loose-price"]/100 != 0.0: embed.add_field(name="Loose Price:", value="$"+str(getresult["products"][page]["loose-price"]/100), inline=True)
                    if getresult["products"][page]["cib-price"]/100 != 0.0: embed.add_field(name="CIB Price:", value="$"+str(getresult["products"][page]["cib-price"]/100), inline=True)
                    if getresult["products"][page]["new-price"]/100 != 0.0: embed.add_field(name="NEW Price:", value="$"+str(getresult["products"][page]["new-price"]/100), inline=True)
                    embed.add_field(name="Search Query", value=search, inline=True)
                    embed.add_field(name="Result", value=str(page + 1) + "/" + str(len(getresult["products"])), inline=True)
                    embed.add_field(name="Get more info about this game", value="https://www.pricecharting.com/game/" + str(getresult["products"][page]["id"]), inline=False)
                    await message.edit(embed=embed)
        else: await channel.send("Something went wrong, please try again")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        embed = message.embeds[0].fields
        page = str(embed[len(embed)-2].value).split('/')
        if payload.emoji.name == "\u2B05": #Left
            if payload.member.id != self.bot.user.id:
                await message.remove_reaction(payload.emoji, payload.member)
                if int(page[0]) > 1:
                    await self.changeCheckPage(embed[len(embed)-3].value, channel, message,  page=int(page[0])-2)
        if payload.emoji.name == "\u27A1": #Right
            if payload.member.id != self.bot.user.id:
                await message.remove_reaction(payload.emoji, payload.member)
                await self.changeCheckPage(embed[len(embed)-3].value, channel, message,  page=int(page[0]))


def setup(bot):
    bot.add_cog(Pricechecker(bot))
