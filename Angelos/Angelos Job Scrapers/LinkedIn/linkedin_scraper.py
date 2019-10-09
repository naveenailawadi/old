from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import csv
import datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import math

# initial website
website = 'https://www.linkedin.com/'

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
et = int(max_count * 8.5) + (int(math.trunc(max_count / 25)) * 4) + 14
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to scrape for jobs on LinkedIn.')

# open a webdriver
driver = webdriver.Safari()
driver.get(website)
print('opened LinkedIn')
time.sleep(3)

# maximize window
driver.maximize_window()

# create a function to search for jobs


def search_jobs(job, city, state):
    find_button = driver.find_element_by_xpath('//button[@class="search__placeholder--search search-input"]')
    time.sleep(2)
    find_button.click()
    time.sleep(1)
    job_box = driver.find_elements_by_xpath('//input[@name="keywords"]')[1]
    time.sleep(2)
    job_box.send_keys(job)
    time.sleep(3)
    location_box = driver.find_elements_by_xpath('//input[@name="location"]')[1]
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
    '''
    submit_button = driver.find_elements_by_xpath('//button[@data-searchbar-type="JOBS"]')
    time.sleep(1)
    submit_button.click()
    time.sleep(1)
    '''
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
* NOT Sponsored (yes or no)
* Job Post URL
* Seniority
* Source (LinkedIn) 

card xpath = //div[@class="jobsearch-SerpJobCard unifiedRow row result clickcard"]
'''

# create a function to gather the cards for each job


def grab_cards():
    card_list = driver.find_elements_by_xpath('//a[@class="result-card__full-card-link"]')
    time.sleep(7)
    return card_list


# create a function to scrape each card


def scrape_card(tag):
    # expand card information
    tag.click()
    time.sleep(1)
    tree_str = '//section[@class="results__detail-view"]'
    # parse the supplemental tree for information
    job_title = driver.find_element_by_xpath('//h2[@class="topcard__title"]').text
    time.sleep(0.5)
    try:
        company_name = driver.find_element_by_xpath('//a[@class="topcard__org-name-link"]').text
        time.sleep(0.5)
    except NoSuchElementException:
        company_name = driver.find_element_by_xpath('//span[@class="topcard__flavor"]').text
        time.sleep(0.5)
    company_review = 'N/A'
    location = driver.find_element_by_xpath('//span[@class="topcard__flavor topcard__flavor--bullet"]').text
    time.sleep(0.5)
    # exp_tags = []

    # create a list of keywords to find
    # keywords = ['experience', 'skills', 'certifications', 'qualifications', 'requirements', 'education', 'abilities', 'required']

    # get all the p and ul tags to parse through
    # p_tags = driver.find_elements_by_xpath(tree_str + '//p')
    # time.sleep(1)
    ul_tags = driver.find_elements_by_xpath('//div[@class="description__text description__text--rich"]')
    time.sleep(1)

    # join the lists of p and ul tags (and convert them to strings)
    # tags = []

    # make a list for the requirements (will be filled)
    requirement_list = []
    # for obj in p_tags:
    # tags.append(obj.text)

    for obj in ul_tags:
        # tags.append(obj.text)
        try:
            requirement_list.append(obj.text)
        except StaleElementReferenceException:
            continue

    # find 4 key criteria
    key_criteria = driver.find_elements_by_xpath('//li[@class="job-criteria__item"]')
    time.sleep(2)

    # get part-time or full time info
    employment_tag = key_criteria[1]
    commitment = employment_tag.find_element_by_xpath('//span[@class="job-criteria__text job-criteria__text--criteria"]').text

    # get job post date
    try:
        job_post_date_raw = str(tag.find_element_by_xpath('//span[@class="topcard__flavor--metadata posted-time-ago__text"]').text + '; Found on: ' + str(day) + '/ ' + str(month) + '/ ' + str(year))
        time.sleep(1)
    except NoSuchElementException:
        job_post_date_raw = 'N/A'

    # refine job date
    if 'day' in job_post_date_raw.lower():
        important = job_post_date_raw.split(' ')[0]
        if '30+' in str(important):
            job_post_date = 'more than a month ago'
        else:
            job_post_day = str(day - int(important))
            job_post_date = str(job_post_day) + '/' + str(month) + '/' + str(year)
    if 'week' in job_post_date_raw.lower():
        important = job_post_date_raw.split(' ')[0]
        job_post_day = str(day - int(important) * 7)
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
    sponsored = 'N/A'

    # seniority
    seniority_tag = key_criteria[0]
    seniority = seniority_tag.find_element_by_xpath('//span[@class="job-criteria__text job-criteria__text--criteria"]').text

    # get the link
    try:
        link = driver.find_element_by_xpath('//a[@data-tracking-control-name="guest_job_details_apply_link_offsite"]').get_attribute('href')
        time.sleep(1)
    except NoSuchElementException:
        link = 'Easy apply at: ' + str(driver.find_element_by_xpath('//a[@data-tracking-control-name="guest_job_details_topcard_title"]').get_attribute('href'))
        time.sleep(0.5)

    # assign source
    source = 'LinkedIn'

    # create a list to centralize all of the information
    card_info = [job_title, company_name, company_review, location, requirement_list, commitment, job_post_date, sponsored, link, seniority, source]
    return card_info


# create a next page function (will be used while the count has not been exceeded)

def next_page():
    next_button = driver.find_element_by_xpath('//button[@class="see-more-jobs"]')
    time.sleep(2)
    next_button.click()
    time.sleep(2)
    return


# search for the jobs
search_jobs(job, city, state)


count = 0

# get to the bottom of the page

# establish a card count
card_count = 25

while True:
    try:
        next_page()
    except NoSuchElementException:
        print('No more pages are available. only ' + str(card_count) + ' jobs are available.')
        max_count = card_count
    card_count += 25
    if card_count >= max_count:
        break

# create a master list to add to the csv
master_list = []

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


driver.close()
print('Done!')
