'''
This script is designed to pull many objects in JSON from an api.
It then formats it into a csv file.
This was done to research the every screensaver that roku had to offer.
'''

import requests
from bs4 import BeautifulSoup as bs
import json
import pandas as pd
import csv

# obtain the channel and key --> input to csv (see key_finder.py)
# then read the keys and iterate for each one

# name csv that will be written
new_file = 'roku_extracted_data.csv'

# api main URL
main_site = 'https://channelstore.roku.com/api/v6/channels/detailsunion/'


# find necessary csv
name = 'name_and_key.csv'

# read csv data and create a list of it
data = pd.read_csv(name, header=0)

# read csv and find keys
keys = data.key


def json_parser(key):
    # create alterated webkey
    website_alt = str(main_site + str(key))

    # create soup
    print('creating soup for ' + website_alt + '...')
    print('Do not touch anything.')
    site_raw = requests.get(website_alt)
    site_soup = bs(site_raw.text, "html.parser")

    # convert website string to json
    json_final = json.loads(site_soup.text)

    # parse json for pertinent data
    # create variables for pertinent data
    name = json_final['feedChannel']['name']
    starRating = json_final['feedChannel']['starRating']
    starRatingCount = json_final['feedChannel']['starRatingCount']
    description = json_final['feedChannel']['description']
    screenshotUrls = json_final['feedChannel']['screenshotUrls']
    screenshotUrls_length = len(screenshotUrls)
    paymentSchedule = json_final['feedChannel']['paymentSchedule']
    priceAsNumber = json_final['details']['priceAsNumber']
    developerUserId = json_final['details']['developerUserId']
    developerId = json_final['details']['developerId']
    isPublic = json_final['details']['isPublic']
    channelState = json_final['details']['channelState']
    name_detail = json_final['details']['name']
    fixedName = json_final['details']['fixedName']
    createdDate = json_final['details']['createdDate']
    modifiedDate = json_final['details']['modifiedDate']
    publishedDate = json_final['details']['publishedDate']
    effectiveAdditionalRequirements = json_final['details']['effectiveAdditionalRequirements']
    literalRevenueSources = json_final['details']['currentDetail']['literalRevenueSources']

    # create list for all of the data (will be loaded into pandas dataframe and master csv)
    data_list = [
        name,
        starRating,
        starRatingCount,
        description,
        screenshotUrls,
        screenshotUrls_length,
        paymentSchedule,
        priceAsNumber,
        developerUserId,
        developerId,
        isPublic,
        channelState,
        name_detail,
        fixedName,
        createdDate,
        modifiedDate,
        publishedDate,
        effectiveAdditionalRequirements,
        literalRevenueSources
    ]
    return data_list


# count potential errors in parsing JSON data
error_count = 0

# create a csv file
with open(str(new_file), mode='w') as csv_file:
    # set up master csv writer
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # iterate over all of the keys
    for key in keys:
        try:
            new_row = json_parser(key)
            writer.writerow(new_row)
        except UnicodeEncodeError:
            error_count += 1
            continue
print('Could not find data for ' + str(error_count) + ' screensavers.')
print('Done!')
