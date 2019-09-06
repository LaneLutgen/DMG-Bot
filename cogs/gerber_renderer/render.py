from discord.ext import commands
import os
from gerber import PCB
from gerber.render import theme
from gerber.render.cairo_backend import GerberCairoContext
from zipfile import ZipFile
import discord
import shutil

class Render(commands.Cog):
    """Renders gerber files as images"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["gerber", "render" "oshparkme"])
    async def render(self, ctx):
        """Renders gerber files as images"""

        GERBER_FOLDER = os.getcwd() + "/cogs/gerber_renderer/gerbers/"
        cairoCTX = GerberCairoContext()
        pcb = PCB.from_directory(GERBER_FOLDER)
        try:
            filename = str(ctx.message.attachments[0].filename)
            filepath = os.getcwd() + "/cogs/gerber_renderer/"
            if filename.endswith(".zip"):
                print("Starting gerber rendering")
                try:
                    await ctx.message.attachments[0].save(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename, use_cached=False)
                    ZipFile(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename).extractall(os.getcwd() + "/cogs/gerber_renderer/gerbers/")
                    os.remove(os.getcwd() + "/cogs/gerber_renderer/gerbers/" + filename)
                    cairoCTX.render_layers(pcb.top_layers, os.getcwd() + "/cogs/gerber_renderer/pcb_top.png", theme.THEMES['OSH Park'], max_width=800, max_height=600)
                    cairoCTX.render_layers(pcb.bottom_layers, os.getcwd() + "/cogs/gerber_renderer/pcb_bottom.png",theme.THEMES['OSH Park'], max_width=800, max_height=600)
                    cairoCTX.render_layers(pcb.copper_layers + pcb.drill_layers,os.getcwd() + "/cogs/gerber_renderer/pcb_transparent_copper.png", theme.THEMES['Transparent Copper'], max_width=800, max_height=600)
                    print("Cairo rendering done")
                    shutil.rmtree(filepath + "gerbers")
                    os.makedirs(filepath + "gerbers")
                    await ctx.send("PCB Top Render", file=discord.File(filepath + "pcb_top.png"))
                    await ctx.send("PCB Bottom Render", file=discord.File(filepath + "pcb_bottom.png"))
                    await ctx.send("PCB Copper Render", file=discord.File(filepath + "pcb_transparent_copper.png"))
                    os.remove(filepath + "pcb_top.png")
                    os.remove(filepath + "pcb_bottom.png")
                    os.remove(filepath + "pcb_transparent_copper.png")
                except:
                    await ctx.send("⚠️ Something went wrong attempting to render, please check your gerbers or try again.")
            else:
                await ctx.channel.trigger_typing()
                await ctx.send("⚠️ File is not a valid .zip file.")
        except IndexError:
            await ctx.send("⚠️ Could not find any attached files, or failed to download file, please try again.")

def setup(bot):
    bot.add_cog(Render(bot))
