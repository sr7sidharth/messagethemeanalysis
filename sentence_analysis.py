import discord
from google.cloud import language_v1
from google.cloud.language_v1 import enums

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

'''
def message_list_to_text(message_list):
    result = ""
    for i in message_list:
        result += ".\n" + i
    return result
'''

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith("fuck you"):
        await message.channel.send("no u")

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
                        final += key + " " + str(value) + "\n"
                if len(final) > 0:
                    await message.channel.send(final)
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
                    final += key + " " + str(value) + "\n"
            if len(final) > 0:
                await message.channel.send(final)
            else:
                await message.channel.send("None of " + message.author.username + "'s messages have more than 20 words...")
            


client.run('NzU1MTY0Mzc5MzU5NjA4OTEz.X1_Tog.fpHPEYxry0QmUsd6re7YS3FYYjw')

