'''
This program will analyze a gmail inbox to find the most frequent
sources of mail. This can be helpful when trying to clean out an inbox.
'''


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from collections import Counter
import time
import math

# raw gmail info
url = 'https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin'
# usr = input('What is the outlook username? \n')
# pwd = input('What is the outlook password? \n')
usr = input('What is your gmail username?')
pwd = input('What is your password?')

# open webdriver
driver = webdriver.Chrome()
driver.get(url)
print('opened gmail')
time.sleep(3)

# enter username
username_box = driver.find_element_by_xpath("//input[@id='identifierId']")
username_box.send_keys(usr)
time.sleep(5)
username_box.send_keys(Keys.ENTER)
time.sleep(2)
print("Email Id entered")

# enter password
password_box = driver.find_element_by_xpath("//input[@type='password']")
password_box.send_keys(pwd)
time.sleep(5)
print("Password entered")
password_box.send_keys(Keys.ENTER)
time.sleep(2)
print('Signed in')

# puts more emails on a page, so it works faster
expander_button = driver.find_element_by_xpath("//div[@class='Wm']")
expander_button.click()
time.sleep(3)
email_range = driver.find_elements_by_xpath("//span[@class='ts']")
time.sleep(2)

# find the number of emails
num_emails_texts = [x.text for x in email_range]
print('Page range found')
num_emails_text = num_emails_texts[2]
num_emails = float(num_emails_text.replace(',', ''))
num_pages_raw = num_emails / 50
num_pages = int(round(num_pages_raw))

# print estimated time
et = num_pages * 10
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to analyze your email inbox.')

# create a list of senders (will be really long)
sender_list = []
for i in range(num_pages):
    senders = driver.find_elements_by_xpath("//span[@class='zF']")
    time.sleep(2)
    for source in senders:
        sender_list.append(source.text)
    print('all senders tabulated')
    next_buttons = driver.find_elements_by_xpath("//div[@aria-label='Older']")
    time.sleep(2)
    if len(next_buttons) > 1:
        next_button = next_buttons[1]
        time.sleep(1)
    else:
        next_button = next_buttons[0]
        time.sleep(1)
    next_button.click()
    time.sleep(3)
    print('going to next page')

# count and sort items in the list
c = Counter(sender_list)
c_sorted = c.most_common()

for group in c_sorted:
    number_of_emails = c[group]
    if number_of_emails > 1:
        line = str(group + ' - ' + str(number_of_emails))
    else:
        line = str(group)
    print(line)
