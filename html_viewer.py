# The HTML Viewer

from bs4 import BeautifulSoup as bs
import requests


def html_viewer():
    # get the site
    website = str(input('What article do you want to read? \
Paste the link below. \n'))

    # name the site
    name = str(input('What do you want to call it?\n'))

    # create soup
    print('creating soup...')
    print('Do not touch anything.')
    site_raw = requests.get(website)
    site_soup = bs(site_raw.text, "html.parser")
    HTML = str(site_soup)
    # write document
    print('writing document... \n')
    doc = open(name + ".txt", "w")
    doc.write(HTML)
    print('Your file has been created. \n It is called ' + name + '.txt')
    print('It will be found in finder under All My Files. \n')


# RUN IT
html_viewer()

# rerun?
answer = str(input('If you view another html, type "yes" and hit enter. \
Otherwise, type "no". \n'))
if 'yes' in answer.lower():
    html_viewer()
else:
    print('Enjoy!')
