import discord
from google.cloud import language_v1
from google.cloud.language_v1 import enums

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$themeAnalysis'):
        messages = await message.channel.history(limit=10000).flatten()
        #msg_content = message.content.strip()
        if message.mentions:
            for user in message.mentions:
                for x in messages:
                    if x.author.id == user.id:
                        #doing something
                await message.channel.send("HI!!!")
        else:
            #use message author messages


client.run('NzU1MTY0Mzc5MzU5NjA4OTEz.X1_Tog.fpHPEYxry0QmUsd6re7YS3FYYjw')

