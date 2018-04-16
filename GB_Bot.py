import discord
import os
import sys
import json

if os.path.isfile('/home/pi/GameBoyBot/config.json') == False:
    file = open('/home/pi/GameBoyBot/config.json', 'w+')
    sys.exit('Created Config file')
else:
    print('Config Present')

with open('/home/pi/GameBoyBot/config.json', 'r', encoding='utf-8') as config_file:
    config = config_file.read()
    config = json.loads(config)
    print('Loaded Config file')

token = (config['Token'])
if token == '':
    sys.exit('No Token provided')
pfx = (config['Prefix'])

cH = (config['Channel'])
if cH == '':
    sys.exit('No Channel provided')

class TestBot(discord.Client):
    def __init__(self):
        super().__init__()

    async def on_ready(self):
        print('===========================================')
        print('DMG 1.0 By HDR')
        print('Logged in as', self.user.name)
        print('===========================================')

    async def on_message(self, message):
        TChannel = self.get_channel(cH)

        if message.content.startswith(pfx):
            Newmsg = str(message.content).replace(pfx, "")
            await self.delete_message(message)
            async for message in self.logs_from(TChannel, limit=50):
                if message.author == self.user:
                    msgID = message.id
                    msg = await self.get_message(TChannel, msgID)
                    await self.edit_message(msg, new_content=Newmsg)

        elif message.content.startswith("ph" + pfx):
            await self.send_message(message.channel, "Placeholder Message")

bot = TestBot()
bot.run(token)
