import discord

client = discord.Client()

#341464294132678668 - general uci chat

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
                count = 0
                boomer_themed_message = 0
                for x in messages:
                    if x.author.id == user.id:
                        count += 1
                        for word in back_in_my_days_vocab:
                            if word in x.content:
                                boomer_themed_message += 1
                                break   
                await message.channel.send("Number of boomer themed messages: " + str(boomer_themed_message) + " in " + str(count) + " messages.")


client.run('NzU1MTY0Mzc5MzU5NjA4OTEz.X1_Tog.fpHPEYxry0QmUsd6re7YS3FYYjw')

#https://www.datamuse.com/api/
#https://cloud.google.com/natural-language/docs/basics
#https://rapidapi.com/RxNLP/api/text-mining-and-nlp
