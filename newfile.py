from cgitb import reset
from email import contentmanager
from xml.etree.ElementTree import C14NWriterTarget
import requests
import json
from datetime import date

today = date.today()
today = today.strftime("%d %B, %Y")
today = today + " \n"

# url = "https://swarajyamag.com/api/v1/stories/286a29af-cf8e-4a61-9f08-7ddc71f798b4"

url = input('Enter API URL: \n')
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

TopFile = open('./textfiles/first.html','r')
thirdfile = open('./textfiles/third.html','r').readlines()
BottomFile = open('./textfiles/second.html','r')

TopLines = TopFile.readlines()
BottomLines = BottomFile.readlines()

CardFirstLine = open('./textfiles/CardParts/first.html','r').readlines()
CardHeadingLine = open('./textfiles/CardParts/heading.html','r').readlines()
CardSecondLine = open('./textfiles/CardParts/second.html','r').readlines()
CardThirdLine = open('./textfiles/CardParts/third.html','r').readlines()
CardFourthLine = open('./textfiles/CardParts/fourth.html','r').readlines()

LinkFirstLine = open('./textfiles/ShareButtonParts/first.html').readlines()
LinkSecondLine = open('./textfiles/ShareButtonParts/second.html').readlines()
LinkThirdLine = open('./textfiles/ShareButtonParts/third.html').readlines()
LinkFourthLine = open('./textfiles/ShareButtonParts/fourth.html').readlines()


CardsFinal = []
CardsFinal  = CardsFinal + TopLines
SecondArticleURL = ArticleURL
ArticleURL = 'href="' + ArticleURL + '" \n'
CardsFinal.append(ArticleURL)
CardsFinal  = CardsFinal + thirdfile
CardsFinal.append(today)
for data in CardParameters:
    CardsFinal = CardsFinal + CardFirstLine
    CardsFinal.append(data['Title'])
    CardsFinal = CardsFinal +  CardHeadingLine                   
    Image = ' src="https://gumlet.assettype.com/' + data['ImageURL'] + '"' + '\n'
    CardsFinal.append(Image)
    Caption = 'alt="' + data['ImageCaption'] + '"' + '\n'
    CardsFinal.append(Caption)
    CardsFinal = CardsFinal + CardSecondLine
    CardsFinal.append(data['ImageCaption'])
    CardsFinal = CardsFinal + CardThirdLine
    CardsFinal.append(data['Content'])
    CardsFinal  = CardsFinal + CardFourthLine

CardsFinal = CardsFinal + LinkFirstLine
# facebook href
facebookline = 'href="https://www.facebook.com/sharer/sharer.php?u=' + SecondArticleURL + '"' + '\n' 
CardsFinal.append(facebookline)
CardsFinal = CardsFinal + LinkSecondLine

# Twitter href
twitterline = 'href="https://twitter.com/intent/tweet?url=' +  SecondArticleURL + '"' + '\n'
CardsFinal.append(twitterline)
CardsFinal = CardsFinal + LinkThirdLine

# Linekdin href
linkedinline = 'href="https://www.linkedin.com/sharing/share-offsite/?url=' + SecondArticleURL + '"' + '\n'
CardsFinal.append(linkedinline)
CardsFinal = CardsFinal + LinkFourthLine

# Email href
CardsFinal = CardsFinal + BottomLines

# f = open("demofile2.html", "a")

# for line in CardFinal:
#     print(line)
# f.close()

OutputFileName = input("Enter the name of output file ending with .html\n")
dummyname = OutputFileName
OutputFileName = "./Outputs/" + OutputFileName
with open(OutputFileName, 'w') as filehandle:
    for line in CardsFinal:
        filehandle.write(line)

print("Output File is Ready as "+ dummyname+"!!")

