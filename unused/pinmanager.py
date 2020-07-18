import datetime
import discord
from discord import DMChannel
from config import get_section
from discord.ext import commands


class Pinmanager(commands.Cog):

    least_role_needed = get_section("bot").get("admin_minimum_role")

    def __init__(self, bot):
        self.bot = bot

    def has_at_least_role(name):
        def predicate(ctx):
            msg = ctx.message
            ch = msg.channel
            if type(ch) == DMChannel:
                return False

            role = discord.utils.get(ctx.guild.roles, name=name)

            return any([x >= role for x in msg.author.roles])

        return commands.check(predicate)

    @commands.command(aliases=["cpin", "clean"])
    @has_at_least_role(least_role_needed)
    async def clearPins(self, ctx):
        removedPins = 0
        await ctx.send("Attempting to remove old pins, this may take a while")
        async for msg in ctx.message.channel.history(limit=5000):
            if (msg.pinned & ((datetime.datetime.now() - msg.created_at).days > 30)):
                    await msg.unpin()
                    removedPins = removedPins + 1
        await ctx.send("Removed " + str(removedPins) + " old pins!")


def setup(bot):
    bot.add_cog(Pinmanager(bot))
