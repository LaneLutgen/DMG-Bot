import os
from discord.ext import commands

from os import listdir
from os.path import isfile, join

import traceback
import config


# Check config
configFile = os.getcwd() + "/config.json"

# Where extensions are stored
cogs_dir = "cogs"

# if not os.path.isfile(configFile):
#     file = open("config.json", "w+")
#     sys.exit("""Created config.json.
# Please enter bot info in the config file before continuing.""")
# with open(configFile) as f:
#     config = json.load(f)
#     print("Loaded config.json.")    
#     if not "token" in config:
#         sys.exit("No token provided in config.")
#     token = config["token"]
# print("Config OK")

prefix = "<@419539233850785792> "


# Bot
bot = commands.Bot(command_prefix='?')

@bot.event
async def on_ready():
    print("""=========================
        DMG Bot
Logged in as {}
=========================""".format(bot.user.name))

# @client.event
# async def on_message(message):
#     if message.content.startswith(prefix): message.content = message.content.split(prefix)[1]

#     if message.content.startswith("resources"):
#         newText = message.content.split("resources")[1]
#         for x in message.author.roles:
#             if x.name == "Yokoi Watch": break
#         else:
#             await client.send_message(message.channel, "You do not have permission to do that.")
#             return
#         await client.delete_message(message)
#         async for x in client.logs_from(message.channel, 10):
#             if x.author == client.user:
#                 await client.edit_message(x, newText)
#                 break


if __name__ == "__main__":
    for extension in ["cogs."+f.replace(".py","") for f in listdir("cogs") if isfile(join("cogs", f))]:
        try:
            bot.load_extension(extension)
            print(f"Loaded extension {extension}")
        except Exception as e:
            print(f'Failed to load extension {extension}.')
            traceback.print_exc()

bot.run(config.BOT_KEY)
