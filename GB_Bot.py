from discord.ext import commands
from discord import Game

import traceback
from config import get_section

# Enter extensions you want to load here
extensions = get_section("bot").get("extensions")

if __name__ == "__main__":
    bot = commands.Bot(command_prefix=get_section("bot").get("command_prefix", "!"),pm_help=True)

    @bot.event
    async def on_ready():
        print('Connected!')
        print(f'Username: {bot.user.name}')
        print(f'ID: {bot.user.id}')
        await bot.change_presence(activity=Game(name="Retro Games"))

    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

    print("Connecting to discord")
    bot.run(get_section("bot").get("discord_key"))
