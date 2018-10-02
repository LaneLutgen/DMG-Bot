import discord
import os
import sys
import json
from random import randint
import requests
import math

# Check config
configFile = os.path.dirname(__file__) + "config.json"

if not os.path.isfile(configFile):
    file = open("config.json", "w+")
    sys.exit("""Created config.json.
Please enter bot info in the config file before continuing.""")
with open(configFile) as f:
    config = json.load(f)
    print("Loaded config.json.")
    if not "token" in config:
        sys.exit("No token provided in config.")
    token = config["token"]
print("Config OK")

prefix = "<@200964739650682881> "


# Bot
client = discord.Client()

@client.event
async def on_ready():
    print("""=========================
        DMG Bot
Logged in as {}
=========================""".format(client.user.name))

@client.event
async def on_message(message):
    if message.content.startswith(prefix): message.content = message.content.split(prefix)[1]

    if message.content.startswith("resources"):
        newText = message.content.split("resources")[1]
        for x in message.author.roles:
            if x.name == "Yokoi Watch": break
        else:
            await client.send_message(message.channel, "You do not have permission to do that.")
            return
        await client.delete_message(message)
        async for x in client.logs_from(message.channel, 10):
            if x.author == client.user:
                await client.edit_message(x, newText)
                break

    elif message.content.startswith("roll"):
        await client.send_typing(message.channel)
        await client.send_message(message.channel, "I rolled a **" + str(randint(1, 6)) + "**")
    
    elif message.content.startswith(("currency", "convert", "cv", "cc")):
        await client.send_typing(message.channel)
        text = message.content.split()
        try:
            value = float(text[1])
            one = text[2].upper()
            two = text[3].upper()
        except:
            await client.send_message(message.channel, "Please format your request properly.")
            return
        request = requests.get("https://free.currencyconverterapi.com/api/v6/convert?q={}_{}&compact=y".format(one, two)).json()
        if not request:
            await client.send_message(message.channel, "Please enter a proper currency.")
            return
        conversion = round(request[one + "_" + two]["val"] * value, 2)
        await client.send_message(message.channel, "{:,}".format(conversion) + " **" + two + "**")

client.run(token)
