from datetime import timedelta

import discord
from discord.ext import commands
import psutil
import os
import time

start_time = time.time()

class Stats(commands.Cog):
	"""Reports server stats."""
	
	def __init__(self, bot):
		self.bot = bot
		
	@commands.command()
	async def stats(self, ctx):
		"""Reports server stats."""
		embed = discord.Embed(title="Server Statistics", color=discord.Color.green())
		embed.add_field(name="Uptime", value=str(timedelta(seconds=int(time.time() - start_time))), inline=False)
		embed.add_field(name="Cores", value=psutil.cpu_count(logical=False), inline=True)
		embed.add_field(name="Threads", value=psutil.cpu_count(), inline=True)
		embed.add_field(name="Usage", value=str(psutil.cpu_percent(interval=None, percpu=True)).replace(",", "%").replace("[", "").replace("]", "%"), inline=False)
		await ctx.channel.trigger_typing()
		await ctx.send(embed=embed)
def setup(bot):
	bot.add_cog(Stats(bot))
