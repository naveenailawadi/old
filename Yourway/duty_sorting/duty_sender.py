'''
This will sort through a desired dataset and send emails to selected subsets.
This was used to email selected employees from a 4000+ row database
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import pandas as pd
import csv

# find the file and make a dataframe
name = input('What is the file called? \n')
data = pd.read_csv(name, header=0)
df = pd.DataFrame(data)
print('DataFrame created')
header_list = df.columns.values.tolist()
# find desired sorting header
while True:
    sorting_choice_str = input('Which header do you want to sort by?\n')
    if sorting_choice_str.lower() in header_list:
        sorting_index = header_list.index(sorting_choice_str)
        print('Header found')
        break
    else:
        print('Column label not found. Please enter again.')

# Create an empty list
Row_list = []

# Iterate over each row
for i in range((df.shape[0])):

    # Using iloc to access the values of
    # the current row denoted by "i"
    Row_list.append(list(df.iloc[i, :]))

print('New list created')

# find desired selections to create a subset
duty_list = []
while True:
    if len(duty_list) > 0:
        print('Your current list is: ')
        print(duty_list)
    new_duty = input('Please enter a selected topic below. (if no more topics are desired, \
type "break loop" to stop inputing.\n')
    if 'break loop' in new_duty:
        break
    elif new_duty.lower() not in duty_list:
        duty_list.append(new_duty)
    else:
        continue

# create an email list
email_list = []
for action in duty_list:
    for i in Row_list:
        if len(i) > 1:
            job = i[sorting_index]
            if action.lower() in job.lower():
                email_list.append(i[0])

# put the email list into a format that can be transferred to a csv
rows = zip(email_list)

# create a backup csv
with open('backup.csv', "w") as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)
print('backup list created. It is called "backup.csv" and is in the same folder as this program.')

# necessary login and email information
usr = input('What is your username? \n')
pwd = input('What is your password? \n')

url = 'https://mail.yourwaytransport.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yourwaytransport.com%2fowa%2f'

title = input('What is the subject of your email?')

body = input('What is the body of your email? (use "\n" to separate paragraphs instead of tabs or returns)')

# open the webdriver
driver = webdriver.Chrome()
driver.get(url)
print('opened outlook')
time.sleep(3)

# enter the login information
username_box = driver.find_element_by_xpath('//input[@id="username"]')
username_box.send_keys(usr)
time.sleep(5)
print("Email Id entered")

password_box = driver.find_element_by_xpath("//input[@id='password']")
password_box.send_keys(pwd)
time.sleep(5)
print("Password entered")

password_box.send_keys(Keys.ENTER)

print('logged in')
time.sleep(3)

# function for sending each individual message


def message_sender(recipient):
    new_message_selection = driver.find_element_by_xpath("//a[@id='newmsgc']")
    time.sleep(2)
    new_message_selection.click()
    time.sleep(1)
    window_before = driver.window_handles[0]
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    time.sleep(3)
    to_box = driver.find_element_by_xpath("//div[@id='divTo']")
    to_box.send_keys(recipient)
    time.sleep(3)
    subject_box = driver.find_element_by_xpath("//input[@id='txtSubj']")
    subject_box.send_keys(title)
    time.sleep(5)
    body_box = driver.find_element_by_xpath("//iframe[@id='ifBdy']")
    body_box.send_keys(body)
    time.sleep(7)
    send_button = driver.find_element_by_xpath("//div[@id='divToolbarButtonsend']")
    send_button.click()
    time.sleep(3)
    driver.switch_to_window(window_before)
    time.sleep(5)
    return


# home URL that can be returned to after sending each email
home = 'https://mail.yourwaytransport.com/owa/'

# print estimated time
num_clients = len(email_list)
et = num_clients * 35
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to send these emails.')

# iterate for each desired email
for client in email_list:
    message_sender(client)
    driver.get(home)
    time.sleep(5)
    print('sent to ' + str(client))

# close the driver when you are done!
driver.close()
print('Done!')
