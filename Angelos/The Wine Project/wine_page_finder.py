from selenium import webdriver
import time
import csv

# open a webdriver
driver = webdriver.Firefox()
time.sleep(5)

# initial website
website = 'https://www.vivino.com/explore?e=eJzLLbI1VMvNzLM1UMtNrLA1NVBLrrQNDVZLBhIuagVAyfQ027LEoszUksQctdxkW7X8JCC2TUktTlYrL4mOBaoAU0YQyhhCmUMoE7Vi25RkAD7lH-w='
driver.get(website)
time.sleep(10)


# infinite scroll --> get to the bottom and load tree
SCROLL_PAUSE_TIME = 3

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# perpetual scroll
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if len(driver.find_elements_by_xpath('//a[@class="anchor__anchor--2QZvA"]')) > 60000:
        break
    last_height = new_height

print('Bottom reached')

# create a list to append with all the wine and their href pairs
href_list = []

# create a function to grab an href from each card


def href_grabber(card):
    wine_href = [card.get_attribute('href')]
    return wine_href


# first grab all of the cards
cards = driver.find_elements_by_xpath('//a[@class="anchor__anchor--2QZvA"]')

for card in cards:
    href = href_grabber(card)
    if href not in href_list:
        href_list.append(href)


# write new file
with open(str('wine_and_wine_page.csv'), mode='w') as csv_file:
    # set up master csv writer
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    header = ['href']
    writer.writerow(header)
    for href in href_list:
        writer.writerow(href)

driver.close()
print('Done!')
