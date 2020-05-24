import os
import discord
import youtube_dl
from discord.ext import commands
from config import get_section
from discord.utils import get


class Music(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        try:
            guild = self.bot.get_guild(id=int(get_section("bot").get("guild")))
            channel = guild.get_channel(int(get_section("music").get("channel")))
            voice = get(self.bot.voice_clients, guild=guild)
            if voice and voice.is_connected():
                await voice.move_to(channel)
            else:
                voice = await channel.connect()
        except Exception as e:
            print(e)

    @commands.command()
    async def play(self, ctx, *, search: str):
        guild = self.bot.get_guild(id=int(get_section("bot").get("guild")))
        commandchannel = guild.get_channel(int(get_section("music").get("commandChannel")))
        if ctx.channel == commandchannel:
            tmp_exists = os.path.isfile("tmp.flac")
            try:
                if tmp_exists:
                    os.remove("tmp.flac")
            except PermissionError:
                await ctx.send("Back in my day we didn't have music queues, we had to wait for other people's music to finish.")
                return

            voice = get(self.bot.voice_clients, guild=ctx.guild)

            params = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'flac',
                    'preferredquality': '384',
                }],
            }

            with youtube_dl.YoutubeDL(params) as ydl:
                ydl.extract_info("ytsearch:" + search)

            for file in os.listdir("./"):
                if file.endswith(".flac"):
                    name = file
                    os.rename(file, "tmp.flac")

            voice.play(discord.FFmpegPCMAudio("tmp.flac"), after=lambda e: print("Song Done!"))
            voice.source = discord.PCMVolumeTransformer(voice.source)
            voice.source.volume = 0.3
            await ctx.send(f"Playing: {name[:-17]}")
            await commandchannel.edit(topic=f"Playing: {name[:-17]}")

    @commands.command(aliases=["vol"])
    async def volume(self, ctx, volume: int):
        guild = self.bot.get_guild(id=int(get_section("bot").get("guild")))
        commandchannel = guild.get_channel(int(get_section("music").get("commandChannel")))
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if ctx.channel == commandchannel and not voice.is_paused():
            if volume not in range(19, 201):
                await ctx.send("Volume has to be between 20 and 200")
            else:
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = float(volume/100)
                await ctx.send("Volume set to " + str(volume))

    @commands.command()
    async def pause(self, ctx):
        guild = self.bot.get_guild(id=int(get_section("bot").get("guild")))
        commandchannel = guild.get_channel(int(get_section("music").get("commandChannel")))
        if ctx.channel == commandchannel:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_playing() and not voice.is_paused():
                voice.pause()
                await ctx.send("Pausing music, run pause command again to resume")
            else:
                if voice.is_paused():
                    voice.resume()
                    await ctx.send("Resuming music")

    @commands.command()
    async def stop(self, ctx):
        guild = self.bot.get_guild(id=int(get_section("bot").get("guild")))
        commandchannel = guild.get_channel(int(get_section("music").get("commandChannel")))
        if ctx.channel == commandchannel:
            voice = get(self.bot.voice_clients, guild=ctx.guild)
            if voice.is_playing() and not voice.is_paused():
                voice.stop()
                await ctx.send("Stopping Music")





def setup(bot):
    bot.add_cog(Music(bot))
