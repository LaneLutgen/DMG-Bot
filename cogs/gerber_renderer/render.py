from discord.ext import commands
import os
from gerber import PCB
from gerber.render import theme
from gerber.render.cairo_backend import GerberCairoContext
from zipfile import ZipFile
import discord
import shutil
import time

class Render(commands.Cog):
    """Renders gerber files as images"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gerber", "render" "oshparkme"])
    async def render(self, ctx):
        """Renders gerber files as images"""

        cairoCTX = GerberCairoContext()
        pcb = PCB.from_directory(os.getcwd() + "/cogs/gerber_renderer/gerbers/")

        async def startrender():
            try:
                print("Starting gerber rendering")
                os.remove(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename)
                time.sleep(5)
                cairoCTX.render_layers(pcb.top_layers, os.getcwd() + "/cogs/gerber_renderer/gerbers/pcb_top.png", theme.THEMES['OSH Park'], max_width=1920, max_height=1080)
                cairoCTX.render_layers(pcb.bottom_layers, os.getcwd() + "/cogs/gerber_renderer/gerbers/pcb_bottom.png", theme.THEMES['OSH Park'], max_width=1920, max_height=1080)
                cairoCTX.render_layers(pcb.copper_layers + pcb.drill_layers,os.getcwd() + "/cogs/gerber_renderer/gerbers/pcb_transparent_copper.png", theme.THEMES['Transparent Copper'], max_width=1920, max_height=1080)
                print("Cairo rendering done")
                await ctx.send("PCB Top Render", file=discord.File(filepath + "gerbers/pcb_top.png"))
                await ctx.send("PCB Bottom Render", file=discord.File(filepath + "gerbers/pcb_bottom.png"))
                await ctx.send("PCB Copper Render", file=discord.File(filepath + "gerbers/pcb_transparent_copper.png"))
            except discord.ext.commands.errors.CommandInvokeError:
                pass
            except UnicodeDecodeError:
                ctx.send("⚠️ An error occurred while attempting to render the gerbers, please check your gerbers.")
        try:
            filename = str(ctx.message.attachments[0].filename)
            filepath = os.getcwd() + "/cogs/gerber_renderer/"
            if filename.endswith(".zip"):
                print("Starting File Unpack")
                try:
                    shutil.rmtree(filepath + "gerbers")
                    os.makedirs(filepath + "gerbers")
                    await ctx.message.attachments[0].save(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename, use_cached=False)
                    with ZipFile(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename) as unzip:
                        #Extract files
                        print("Starting file extraction")
                        unzip.extractall()
                        print("Files Extracted")
                        await startrender()
                except:
                    pass
            else:
                await ctx.channel.trigger_typing()
                await ctx.send("⚠️ File is not a valid .zip file.")
        except IndexError:
            await ctx.send("⚠️ Could not find any attached files, or failed to download file, please try again.")

def setup(bot):
    bot.add_cog(Render(bot))
