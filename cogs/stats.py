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
		
		await ctx.channel.trigger_typing()
		
		temps = psutil.sensors_temperatures()
		await ctx.send('**Runtime:** ' + str(int(round(time.time() - start_time, 10) / (60))) + ' Minutes \n**CPU Load:** ' + str(round(float(os.popen('''grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage }' ''').readline()),2)) + '% \n' + '**CPU Temps:** \n' + str("Core 0: " + "+" + str(temps)[46:50] + "C\n" + "Core 1: " + "+" + str(temps)[112:116] + "C\n" + "Core 2: " + "+" + str(temps)[178:182] + "C\n" + "Core 3: " + "+" + str(temps)[244:248] + "C") + '\n' + '**RAM Usage:** ' + str(psutil.virtual_memory().percent) + '%')
		
def setup(bot):
	bot.add_cog(Stats(bot))
