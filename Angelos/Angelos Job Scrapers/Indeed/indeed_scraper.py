from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import csv
import datetime
from selenium.common.exceptions import NoSuchElementException
import math

# initial website
website = 'https://www.indeed.com/'

# input scraping info (job, city, state)

job = str(input('What is the job that you are looking for? \n'))
city = str(input('What city are you looking for a job in? \n'))
state = str(input('What state (or country) are you looking for a job in (abbreviation)? \n'))

# input file name
file_name = str(input('What is the name of the csv file that will be appended? \n'))
file = file_name + '.csv'

# determine what day it is
dt = datetime.datetime.today()
day = dt.day
month = dt.month
year = dt.year

# create maximum
max_count = int(input('What is the maximum number of jobs that you would like to scrape? \n'))

# print estimated time
et = (max_count * 10) + 14
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to scrape for jobs on Indeed.')

# open a webdriver
driver = webdriver.Safari()
driver.get(website)
print('opened indeed')
time.sleep(3)

# maximize window
driver.maximize_window()

# create a function to search for jobs


def search_jobs(job, city, state):
    job_box = driver.find_element_by_xpath('//input[@id="text-input-what"]')
    time.sleep(2)
    job_box.send_keys(job)
    time.sleep(3)
    location_box = driver.find_element_by_xpath('//input[@id="text-input-where"]')
    time.sleep(2)
    if len(city) >= 1:
        location = str(city + ', ' + state)
    else:
        location = str(state)

    # clear location box
    location_box.send_keys(Keys.COMMAND, "a")
    time.sleep(0.5)
    location_box.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)

    # fill location box
    location_box.send_keys(location)
    time.sleep(2)
    # click enter
    location_box.send_keys(Keys.ENTER)
    time.sleep(1)
    return


'''
FIELDS TO SCRAPE FOR:
* Job Title
* Company Name
* Company Review (#) (rating)
* Location
* Experience (necessary) (keywords: experience, skills, certifications, qualifications, requirements, education, abilities, )
* Job Type (full or part time)
* Post Date
* Sponsored (yes or no)
* Job Post URL
* Source (indeed) 

card xpath = //div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]
'''

# create a function to gather the cards for each job


def grab_cards():
    card_list = driver.find_elements_by_xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]')
    time.sleep(7)
    return card_list


# create a way to sort through the sponsored tags
card_count = 0

# create a function to scrape each card


def scrape_card(tag):
    # expand card information
    tag.click()
    time.sleep(1)
    tree_str = '//div[@id="vjs-container"]'
    # parse the supplemental tree for information
    job_title = driver.find_element_by_xpath('//div[@id="vjs-jobtitle"]').text
    time.sleep(.5)
    company_name = driver.find_element_by_xpath('//span[@id="vjs-cn"]').text
    time.sleep(.5)
    try:
        company_review_big = driver.find_element_by_xpath(tree_str + '//span[@class="ratings"]').get_attribute('aria-label')
        time.sleep(1)
        company_review = str(company_review_big).split(' ')[0]
    except NoSuchElementException:
        company_review = 'N/A'
    location = driver.find_element_by_xpath('//span[@id="vjs-loc"]').text[2:]
    time.sleep(.5)
    # exp_tags = []

    # create a list of keywords to find
    # keywords = ['experience', 'skills', 'certifications', 'qualifications', 'requirements', 'education', 'abilities', 'required']

    # get all the p and ul tags to parse through
    # p_tags = driver.find_elements_by_xpath(tree_str + '//p')
    # time.sleep(1)
    ul_tags = driver.find_elements_by_xpath(tree_str + '//ul')
    time.sleep(1)

    # join the lists of p and ul tags (and convert them to strings)
    # tags = []

    # make a list for the requirements (will be filled)
    requirement_list = []
    # for obj in p_tags:
    # tags.append(obj.text)

    for obj in ul_tags:
        # tags.append(obj.text)
        requirement_list.append(obj.text)
    '''
    # iterate through the p tags to find the right ones
    key_bool = False
    for obj in tags:
        for keyword in keywords:
            if keyword in obj:
                if obj not in exp_tags:
                    exp_tags.append(obj)
                key_bool = True
                continue
        if key_bool:
            if obj not in exp_tags:
                exp_tags.append(tag)
                key_bool = False

    span_tags = driver.find_elements_by_xpath('//div[@id="vjs-container"]//span')
    time.sleep(0.5)

    # iterate through span tags
    for obj in span_tags:
        # get all the requirements into a list
        requirement_list.append(obj.text)
    # create an "N/A entry for the requirements"
    if len(requirement_list) == 0:
        requirement_list.append('N/A')
    '''

    # get part-time or full time info
    div_header_tags = driver.find_elements_by_xpath('//div[@id="vjs-container"]//div//span')
    time.sleep(.5)
    commitment = ''
    for obj in div_header_tags:
        if "time" in obj.text:
            commitment = obj.text
    if len(commitment) == 0:
        commitment = 'N/A'

    # get job post date
    try:
        job_post_date_raw = str(driver.find_element_by_xpath('//div[@id="vjs-container"]//span[@class="date "]').text + '; Found on: ' + str(day) + '/ ' + str(month) + '/ ' + str(year))
        time.sleep(.5)
    except NoSuchElementException:
        job_post_date_raw = 'N/A'

    # refine job date
    if 'today' in job_post_date_raw.lower():
        job_post_date = str(day) + '/' + str(month) + '/' + str(year)
    elif 'day' in job_post_date_raw.lower():
        important = job_post_date_raw.split(' ')[0]
        if '30+' in str(important):
            job_post_date = 'more than a month ago' + '; Found on ' + str(day) + '/' + str(month) + '/' + str(year)
        else:
            job_post_day = str(day - int(important))
            job_post_date = str(job_post_day) + '/' + str(month) + '/' + str(year)
    elif 'month' in job_post_date_raw.lower():
        important = int(job_post_date_raw.split(' ')[0])
        job_post_month = str(month - important)
        job_post_date = str(job_post_month) + '/' + str(year)
    elif 'year' in job_post_date_raw.lower():
        important = int(job_post_date_raw.split(' ')[0])
        job_post_date = str(year - important)
    else:
        job_post_date = job_post_date_raw

    # sponsored?
    try:
        card = driver.find_elements_by_xpath('//div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]//span[@class= " sponsoredGray "]')[card_count]
        sponsored = True
    except IndexError:
        sponsored = False
    except NoSuchElementException:
        sponsored = False

    # get the link
    try:
        link = driver.find_element_by_xpath('//span[@data-indeed-apply-joburl]').get_attribute('data-indeed-apply-joburl')
        time.sleep(1)
    except NoSuchElementException:
        link = driver.find_element_by_xpath('//div[@id="vjs-container"]//div[@id="apply-button-container"]//a').get_attribute('href')
        time.sleep(.5)

    # assign source
    source = 'indeed'

    # create a list to centralize all of the information
    card_info = [job_title, company_name, company_review, location, requirement_list, commitment, job_post_date, sponsored, link, 'N/A', source]
    return card_info

# create a next page function (will be used while the count has not been exceeded)


def next_page():
    move_buttons = driver.find_elements_by_xpath('//span[@class="np"]')
    time.sleep(2)
    if len(move_buttons) > 1:
        next_button = move_buttons[1]
    else:
        next_button = move_buttons[0]
    next_button.click()
    time.sleep(2)
    return


def close_popup():
    try:
        popup_close = driver.find_element_by_xpath('//a[@class="icl-CloseButton popover-x-button-close"]')
        time.sleep(0.5)
        popup_close.click()
        time.sleep(1)
    except NoSuchElementException:
        print('No popup found!')
    return


# search for the jobs
search_jobs(job, city, state)


count = 0
# establish backup count
backup_count = 0

while count <= max_count:
    # fill master list with previous information
    try:
        with open(file, 'r') as f:
            master_list = []
            reader = csv.reader(f)
            old_list = list(reader)
        for cell in old_list:
            master_list.append(cell)
    except FileNotFoundError:
        print('A new file called ' + file + ' will be created.')
        master_list = [['Job Title', 'Company Name', 'Company Review', 'Location', 'Experience', 'Job Type', 'Post Date', 'Sponsored', 'Job Post URL', 'Seniority Level', 'Source']]
    cards = grab_cards()
    for card in cards:
        try:
            info = scrape_card(card)
        except NoSuchElementException:
            time.sleep(5)
            info = scrape_card(card)
        # add info to list if not already there
        # iterate through all cells in master_list
        master_bool = True  # True --> append the master list
        for one_cell in master_list:
            if (info[0] in one_cell[0]) and (info[1] in one_cell[1]):
                master_bool = False
        if master_bool:
            master_list.append(info)
        count += 1
        card_count += 1
        if count > max_count:
            break
    with open(file, mode='w') as csv_file:
        # set up master csv writer
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in master_list:
            writer.writerow(row)
            backup_count += 1
            if backup_count > max_count:
                break
        if backup_count > max_count:
            break
    if count > max_count:
        break

    next_page()
    close_popup()


driver.close()
print('Done!')
