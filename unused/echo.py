from discord.ext import commands
import discord
from discord import TextChannel, HTTPException, DMChannel
import asyncio
import re

from config import get_section


class Echo(commands.Cog):
    """Provides tools that allow moderators to chat through the bot. Useful for managing sticky posts."""

    least_role_needed = get_section("bot").get("admin_minimum_role")

    def __init__(self, bot):
        self.bot = bot
        self.id_regex = re.compile(r"([0-9]{15,21})")

    def has_at_least_role(name):
        def predicate(ctx):
            msg = ctx.message
            ch = msg.channel
            if type(ch) == DMChannel:
                return False

            role = discord.utils.get(ctx.guild.roles, name=name)

            return any([x >= role for x in msg.author.roles])

        return commands.check(predicate)

    @commands.command(aliases=["e"])
    @has_at_least_role(least_role_needed)
    async def echo(self, ctx, target_channel: TextChannel, *, message: str):
        """Echoes a message to a channel"""
        await target_channel.trigger_typing()
        await target_channel.send(message)

    @echo.error
    async def handle_echo_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'target_channel':
                await ctx.send("⚠️ Please specify a channel to echo to.")
            elif error.param.name == "message":
                await ctx.send("⚠️ Please enter a message to echo.")

    @commands.command(aliases=["hist", "h"])
    @has_at_least_role(least_role_needed)
    async def history(self, ctx, target_channel: TextChannel, history_limit=10):
        """Gets the bots message history for a given channel."""
        async with ctx.channel.typing():

            messages = await target_channel.history(reverse=True, limit=history_limit).filter(lambda x: x.author == ctx.me).flatten()

            output = "\n".join([f"{x.id}: {x.clean_content}" for x in messages])

            await ctx.send(f"```{output}```", delete_after=30)

    @history.error
    async def handle_history_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'target_channel':
                await ctx.send("⚠️ Please specify a channel to get history from.")

    @commands.command()
    @has_at_least_role(least_role_needed)
    async def edit(self, ctx, message_link: str, *, edit: str):
        """Edits a given message in a given channel."""
        msgstr = message_link.split("/")
        guild = self.bot.get_guild(int(msgstr[4]))
        channel = guild.get_channel(int(msgstr[5]))
        message = await channel.fetch_message(int(msgstr[6]))

        if message.author == self.bot.user:
            await message.edit(content=edit)


    @echo.error
    async def handle_edit_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'target_channel':
                await ctx.send("⚠️ Please specify the channel the target message is in.")
            elif error.param.name == "target_message":
                await ctx.send("⚠️ Please specify the message you want to edit.")

    @commands.command()
    @has_at_least_role(least_role_needed)
    async def delete(self, ctx, target_channel: TextChannel, target_message: str):
        """Deletes a given message in a given channel."""

        if not self.id_regex.match(target_message):
            await ctx.send(f"⚠ {target_message} is not a valid message id!")
            return

        message_to_delete = await target_channel.get_message(target_message)

        await ctx.send(f"🗑️ {message_to_delete.id} is going to be deleted. Are you sure you want to do that (Y/N)?")

        # Only allow editing by the person who initiated the edit request
        def check(m):
            return m.author == ctx.author

        try:
            answer = await ctx.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
            await ctx.send("⚠ Got no reply, canceling delete.")
        else:
            try:
                if answer.content.lower().startswith(("no", "n", "fuck")):
                    await ctx.send("ℹ Aborting delete.")
                    return
                elif answer.content.lower().startswith(("yes", "n")):
                    await message_to_delete.delete()
                else:
                    await ctx.send("⚠ Got no clear answer, aborting delete.")
                    return
            except HTTPException:
                await ctx.send("⚠ Failed to delete message.")
            else:
                await ctx.send("✅ Message deleted succesfully.")

    @delete.error
    async def handle_delete_errors(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'target_channel':
                await ctx.send("⚠️ Please specify the channel the target message is in.")
            elif error.param.name == "target_message":
                await ctx.send("⚠️ Please specify the message you want to delete.")


def setup(bot):
    bot.add_cog(Echo(bot))
