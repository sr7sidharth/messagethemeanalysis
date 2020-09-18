import discord
import json
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import requests
from bs4 import BeautifulSoup
import random

random.seed()
image_get_url = "http://www.google.com/search"
params_img_get = {
    "tbm" : "isch",
    "q" : ""
}

ud_url = "https://www.urbandictionary.com/define.php"
params_ud = {
    "term" : ""
}

def sample_classify_text(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze. Must include at least 20 words.
    """

    client = language_v1.LanguageServiceClient()

    # text_content = 'That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows.'

    # Available types: PLAIN_TEXT, HTML
    type_ = enums.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    response = client.classify_text(document)
    #print(response)
    # Loop through classified categories returned from the API
    result = dict()
    #cat = ""
    #conf = ""
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        #print(u"Category name: {}".format(category.name))
        #cat += (u"Category name: {}".format(category.name))
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        #print(u"Confidence: {}".format(category.confidence))
        #conf += (u"Confidence: {}".format(category.confidence))
        result[category.name] = category.confidence
    return result


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    """
    Contents of this function trigger upon a new message being typed in a discord channel that the bot has access to

    message: Contains the discord message object that triggered this event
    """
    #Check if the event was triggered by the bot
    if message.author == client.user:
        return

    #Uses webscraping concepts to send a picture of the input search term (that follows '$searchpic')
    if message.content.startswith("$searchpic"):
        params_img_get["q"] = message.content[11:]
        req = requests.get(image_get_url, params = params_img_get)
    
        soup = BeautifulSoup(req.text, features="html.parser")
        results = []
        random_index = random.randrange(1, 15)
        '''
        results = soup.findAll('img')[1:4]
        for i in results:
            await message.channel.send(i['src'])
        '''
        await message.channel.send(soup.findAll('img')[random_index]['src']) #Issue with this is, the pictures are not the full res versions - need to click on the image and then copy that image address
        #await message.channel.send(file = discord.File("test_pic_gc.jpg")) #use files = array of Discord File objects for multiple pics
        #await message.channel.send("https://i.imgur.com/TXVEc7N.jpg") #uses Discord's feature of turning image links into In-App previews of the image

    #Urban dictionary word search
    if message.content.startswith("$ud"):
        params_ud["term"] = message.content[4:]
        req = requests.get(ud_url, params = params_ud)

        soup = BeautifulSoup(req.text, features="html.parser")
        for i in soup.findAll('meta'):
            if 'content' in i.attrs and 'name' in i.attrs:
                if i['name'] == 'Description':
                    await message.channel.send(i['content'])

    #Uses Google Natural Language API to associate user messages with themes and sends the top 3 most common themes
    if message.content.startswith('$themeAnalysis'):
        messages = await message.channel.history(limit=10000).flatten()
        #msg_content = message.content.strip()
        if message.mentions:
            for user in message.mentions:
                result = dict()
                for x in messages:
                    if x.author.id == user.id:
                        if len(x.content.split()) > 20:
                            temp_dict = sample_classify_text(x.content)
                            for key,value in temp_dict.items():
                                if key in result:
                                    result[key] = (result[key] + value)/2
                                elif key not in result:
                                    result[key] = value
                sorted_result = sorted(result.items(), key=lambda x : x[1], reverse = True)
                final = ""
                index = 0
                for key,value in sorted_result:
                    if index == 3:
                        break
                    else:
                        index += 1
                        final += str(index) + ". " + str(key)[1:] + "\n"
                if len(final) > 0:
                    await message.channel.send("The top 3 themes of "+ str(user) + "'s messages are:\n" + final)
                else:
                    await message.channel.send("None of " + str(user) + "'s messages have more than 20 words...")
        else:
            #use message author messages
            result = dict()
            for x in messages:
                if x.author.id == message.author.id:
                    if len(x.content.split()) > 20:
                        temp_dict = sample_classify_text(x.content)
                        for key,value in temp_dict.items():
                            if key in result:
                                result[key] = (result[key] + value)/2
                            elif key not in result:
                                result[key] = value
            sorted_result = sorted(result.items(), key=lambda x : x[1], reverse = True)
            final = ""
            index = 0
            for key,value in sorted_result:
                if index == 3:
                    break
                else:
                    index += 1
                    final += str(index) + ". " + str(key)[1:] + "\n"
            if len(final) > 0:
                await message.channel.send("The top 3 themes of "+ str(message.author) + "'s messages are:\n" + final)
            else:
                await message.channel.send("None of " + str(message.author) + "'s messages have more than 20 words...")
            

client.run('NzU1MTY0Mzc5MzU5NjA4OTEz.X1_Tog.fpHPEYxry0QmUsd6re7YS3FYYjw')