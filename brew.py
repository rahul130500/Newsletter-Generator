from cgitb import reset
from email import contentmanager
from xml.etree.ElementTree import C14NWriterTarget
import requests
import json
from datetime import date

today = date.today()
today = today.strftime("%d %B, %Y")
today = today + " \n"

url = "https://swarajyamag.com/api/v1/stories/8ddb42ae-a386-4a5a-a052-4a9f4c5dcba2"
CardsFinal = []
# url = input('Enter API URL: \n')
r = requests.get(url)
response = r.json()
storycards = response['story']['cards']

CardParameters = []

ArticleURL = response['story']['url']
ArticleURL = ArticleURL + ""

for element in storycards:
    Title = element['story-elements'][0]['text']
    Title = Title.replace("<a ", '<a style="color: #ce4242; text-decoration: none;" ')
    Title = Title.replace('<strong>','<strong style="color: #ce4242">')
    Title = Title.replace("<ins>",'<ins style="text-decoration: none;">')
    Title  =Title.replace("<p>",'<p style="color: #ce4242">')
    totalsize = len(element['story-elements'])
    Content = ""
    ImageCaption = element['metadata']['social-share']['image']['caption']
    ImageURL = element['metadata']['social-share']['image']['key']
    for i in range(1,totalsize):
        if(element['story-elements'][i]['type']=="text"):
            Content = Content + element['story-elements'][i]['text']
        if(element['story-elements'][i]['type']=="image"):
            ImageCaption = element['story-elements'][i]['title']
            ImageURL = element['story-elements'][i]['image-s3-key']
    Content = Content.replace('<a ','<a style="color: #ce4242; text-decoration: none;" ')
    Content = Content.replace('<strong>','<strong style="color: #ce4242">')
    Content= Content.replace("<ins>",'<ins style="text-decoration: none;">')

    CardObject = {
        "Title":Title,
        "Content":Content,
        "ImageURL":ImageURL,
        "ImageCaption":ImageCaption
    }
    CardParameters.append(CardObject)

MainFile = open('./brewtempfiles/content.html','r').readlines()
CardFile = open('./brewtempfiles/card.html','r').readlines()



def cardEmbedder(object):
    for line in CardFile:
        if(line=="<!-- Heading -->\n"):
            title = object["Title"] + "\n"
            CardsFinal.append(title)
        elif(line=="<!-- Content -->\n"):
            CardsFinal.append(object["Content"])
            CardsFinal.append("\n")
        elif(line=="                <!-- ImageURL -->\n"):
            url  = '                src="https://gumlet.assettype.com/' + object['ImageURL'] + '"' + '\n'
            CardsFinal.append(url)
        elif(line=="<!-- ImageCaption -->\n"):
            CardsFinal.append(object["ImageCaption"])
            CardsFinal.append("\n")
        else:
            CardsFinal.append(line)
    return

for line in MainFile:
    if(line=="<!-- Date -->\n"):
        CardsFinal.append(today)
    elif(line=="<!-- cards -->\n"):
        for object in CardParameters:
            cardEmbedder(object)
    else:
        CardsFinal.append(line)



# OutputFileName = input("Enter the name of output file ending with .html\n")
OutputFileName = "output.html"
dummyname = OutputFileName
OutputFileName = "./Outputs/" + OutputFileName
with open(OutputFileName, 'w') as filehandle:
    for line in CardsFinal:
        filehandle.write(line)

print("Output File is Ready as "+ dummyname+"!!")

