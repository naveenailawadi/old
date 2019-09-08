'''
This program reads any website to you. This can turn articles
into much friendlier podcasts.
It will export the speech to an mp3, which is easily
playable and exportable.
'''

from gtts import gTTS
from bs4 import BeautifulSoup as bs
import requests

# function to grab important parts of the website


def html_to_speech():
    # get the site
    website = str(input('What article do you want to listen to? \
Paste the link below. \n'))

    # create a master string to be added to
    master_string = ''

    # create soup
    print('creating soup...')
    print('Do not touch anything.')
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")

    for header in site_soup.find_all('h1'):
        master_string += header.text
        master_string += '\n'
    for p in site_soup.find_all('p'):
        master_string += p.text
        master_string += '\n'
    return master_string


# Language in which you want to convert
language = 'en'

# call the function
my_text = html_to_speech()

# Passing the text and language to the engine,
# here we have marked slow=False. Which tells
# the module that the converted audio should
# have a high speed
myobj = gTTS(text=my_text, lang=language, slow=False)


# name the file
name = str(input('What would you like to call the mp3 file? \n') + '.mp3')
# Saving the converted audio in a mp3 file named
# welcome
myobj.save(name)
print('mp3 saved')
