import discord
from discord.ext import commands


class Quote(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def quote(self, ctx, *, quote: str):
        quoteStr = quote.split("/")
        guild = self.bot.get_guild(int(quoteStr[4]))
        channel = guild.get_channel(int(quoteStr[5]))
        message = await channel.fetch_message(int(quoteStr[6]))
        embed = discord.Embed(title="", color=message.author.colour, description=message.content)
        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url, url=quote)
        embed.set_footer(text="#"+channel.name + " - " + message.created_at.strftime("%d/%m/%Y"))
        await ctx.channel.trigger_typing()
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Quote(bot))
