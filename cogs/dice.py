from discord.ext import commands
import random


class Dice(object):
    """Allows you to throw some dice using standard dice notation."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["dice"])
    async def roll(self, ctx, dicetype: str="1d6"):
        """Rolls a dice using standard dice notation."""

        await ctx.channel.trigger_typing()

        try:
            amount, sides = map(int, dicetype.split("d"))
        except ValueError:
            await ctx.send("⚠️ Incorrect input, use amount**d**sides, e.g. 2d6 (two six sided dice).")
            return

        if(amount <= 0):
            await ctx.send("⚠️ You gotta throw the dice at least once.")
            return

        if(sides <= 1):
            await ctx.send("⚠️ One-sided dice do not exist. Try more sides.")
            return

        result = sum([random.randint(1, sides) for _ in range(amount)])

        await ctx.send(f"🎲 I rolled a {result} for you.")


def setup(bot):
    bot.add_cog(Dice(bot))
