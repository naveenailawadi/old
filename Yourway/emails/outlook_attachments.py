'''
This script does the exact same thing as the email sender, but
it also adds an attachment using its filepath.
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import pandas as pd
import os


# loads the necessary data
name = input('What is the file called? \n(put all the emails in a column headed email) \n')
data = pd.read_csv(name, header=0)
email_list = data.email

# count clients for later
num_clients = len(email_list)

# basic login information etc.
usr = 'yourway/gulam'
pwd = 'takeda110'

url = 'https://mail.yourwaytransport.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yourwaytransport.com%2fowa%2f'

title = 'Premium Courier and Clinical Packaging'

body = 'New meeting requested\n\n\
I would like to introduce you to Yourway, the only true premium courier and clinical packager all in one company. We offer door to door service of any temp control shipment globally with now our own global GMP depot network with primary and secondary packaging, including short and long term storage of 15-25C, 2-8C, -20C and -80C and -180C and distribution.\n\n\
Main facility headquartered in Allentown, Pennsylvania, we also operate 21 other strategically-located GMP depots worldwide. Yourway is a premium courier of time- and temperature-sensitive clinical materials, and offers integrated clinical packaging, storage, and other specialty services.\n\n\
It would be a pleasure to formally introduce myself and tell you more, so I invite you to meet at BIO International, booth #4209. Do you have a good day/time? Or we could schedule a face-to-face that fits your schedule in the Partnering Forum?\n\n\
Sincerely,\n\n\
Gulam Jaffer\n\
President\n\
Yourway Transport, Inc.\n\
6681 Snowdrift Road\n\
Allentown, PA 18106\n\
610.395.9198 Main\n\
610.391.9002 Fax\n\
610.517.2320 Mobile\n\
Email: jaffer@yourwaytransport.com\n\
www.yourway.com'

# open webdriver
driver = webdriver.Chrome()
driver.get(url)
print('opened outlook')
time.sleep(3)

# log in
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

# set attachment
attachment = input('Paste the filepath to the desired attachment below. \n')

# this function sends the message with the attachment


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
    attachment_button = driver.find_element_by_xpath("//div[@id='divToolbarButtonattachfile']")
    time.sleep(2)
    attachment_button.click()
    time.sleep(2)
    choose_file = driver.find_element_by_xpath("//input[@id='file1']")
    time.sleep(2)
    choose_file.send_keys(os.getcwd() + attachment)
    time.sleep(2)
    attach_file = driver.find_element_by_xpath("//button[@id='btnAttch']")
    time.sleep(1)
    attach_file.click()
    time.sleep(2)
    send_button = driver.find_element_by_xpath("//div[@id='divToolbarButtonsend']")
    send_button.click()
    time.sleep(3)
    driver.switch_to_window(window_before)
    time.sleep(5)
    return


# reload the home page after sending each email
home = 'https://mail.yourwaytransport.com/owa/'


# print estimated time
et = num_clients * 46
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to send these emails.')

# iterates the function over all the emails
for client in email_list:
    message_sender(client)
    driver.get(home)
    time.sleep(5)
    print('sent to ' + str(client))

# close the driver after!
driver.close()
print('Done!')
