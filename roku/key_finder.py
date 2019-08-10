'''
This program was used in conjuction with the json parser to obtain
screensaver keys for a roku research project.
This found the key for each of the screensavers and paired it with the
screensaver name. This information was put into a csv file
that would later be read to operate the API and obtain JSON data.
'''

from selenium import webdriver
import time
import csv

# name csv that will be written
new_file = 'name_and_key.csv'
# new_file = str(input("What would you like to call your new csv? \n") + '.csv')

# main website
website = 'https://channelstore.roku.com/browse/screensavers'

# start number id is 28
master_num = 28
count = 1

# set up list of pairs to add to (name, key)
pair_list = []

# open a webdriver
driver = webdriver.Safari()
driver.get(website)
print('opened roku site')
time.sleep(3)


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
    if new_height == last_height:
        break
    last_height = new_height

print('Bottom reached')

# Now that the entire HTML tree has loaded,
# the program will find the different screensaver names and keys
# by parsing through h2 tags.


def key_finder():

    # set a counter
    count = 0
    # find name and key by h2 tags
    tags = driver.find_elements_by_xpath("//h2/a")
    num_elements = len(tags)
    print(str(num_elements) + ' elements found')
    time.sleep(50)
    for element in tags:
        try:
            name_element = element.get_attribute("title")
            name = str(name_element)
            key_element = element.get_attribute("href")
            key_raw = str(key_element)
            key = key_raw.split('/')[4]
            print(name + ', ' + key)
            name_and_key = [name, key]
            # append pair list
            pair_list.append(name_and_key)
            count += 1
        except UnicodeEncodeError:
            continue
    print(str(count) + ' screensavers have been found')


# run the function
key_finder()

# write file
with open(str(new_file), mode='w') as csv_file:
    # set up master csv writer
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    for pair in pair_list:
        writer.writerow(pair)

print('File written')
print('Done!')
