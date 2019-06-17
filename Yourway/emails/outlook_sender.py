'''
Yourway Transport is a biopharmaceutical company that deals with
a vast amount of clientele. Often, the company organizes
meetings with certain clients, but not all of them.
The CEO, Gulam Jaffer, prefers that each email be sent by itself
instead of sending a mass email. As a result, he provided me with a
csv with these emails. This program will send a given body email
with its title to each of the emails on the csv.
**The username and password of the employer have been replaced
with inputs for security purposes**
'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import math
import pandas as pd

name = input('What is the file called? \n(put all the emails in a column headed email) \n')
data = pd.read_csv(name, header=0)
email_list = data.email

# count clients for later
num_clients = len(email_list)

# basic information
usr = 'yourway/gulam'
pwd = 'takeda110'

url = 'https://mail.yourwaytransport.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yourwaytransport.com%2fowa%2f'

title = 'Yourway - Premium Courier and Clinical Packaging'

body = 'New meeting requested\n\n\
I would like to introduce you to Yourway, the only true premium courier and clinical packager all in one company. We offer door to door service of any temp control shipment globally with our own global GMP depot network with primary and secondary clinical packaging, including short and long term storage of 15-25C, 2-8C, -20C and -80C and -180C and distribution. \n\n\
Main facility headquartered in Allentown, Pennsylvania, we also operate 20 other strategically-located GMP depots worldwide. Yourway is a premium courier of time- and temperature-sensitive clinical materials, and offers integrated clinical packaging, storage, and other specialty services. \n\n\
It would be a pleasure to formally introduce myself and tell you more, so I invite you to meet us at The DIA Conference, booth #517. Do you have a good day/time for a meeting at our booth that fits your schedule? Look forward to hearing from you. \n\n\
Thanks'

# open the webdriver
driver = webdriver.Chrome()
driver.get(url)
print('opened outlook')
time.sleep(3)

# enter information
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

# this navigates outlook's website to send a message


def message_sender(recipient):
    new_message_selection = driver.find_element_by_xpath("//a[@id='newmsgc']")
    time.sleep(2)
    new_message_selection.click()
    time.sleep(1)
    # outlook creates a new window, so it must be selected
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


# the original site must be refreshed to send more emails
home = 'https://mail.yourwaytransport.com/owa/'


# print estimated time
et = num_clients * 35
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to send these emails.')

# iterate for all the clients.
for client in email_list:
    message_sender(client)
    driver.get(home)
    time.sleep(5)
    print('sent to ' + str(client))

# close the driver after!
driver.close()
print('Done!')
