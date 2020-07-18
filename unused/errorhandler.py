import discord
from discord.ext import commands
import time
start_time = time.time()


class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send(ctx.invoked_with + " is not a valid command")
        if ctx.command.name is not None:
            cmd = ctx.command.name
            if cmd == "pricecheck":
                if isinstance(error, commands.MissingRequiredArgument):
                    await ctx.send("Please specify a game you want to search for")
                if isinstance(error, commands.CommandOnCooldown):
                    await ctx.send('Sorry, the command is on cooldown for you right now. Try again in ' + str(int(error.retry_after)) + ' seconds')
            if cmd == "quote":
                if isinstance(error, commands.CommandError):
                    await ctx.send("Please specify a valid message link")


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
