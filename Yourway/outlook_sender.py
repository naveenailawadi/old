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
import pandas

name = 'emails.csv'

data = pandas.read_csv(name)
email_list = data.email

# count clients for later
num_clients = len(email_list)

# key_phrase = input('What category would you like to make requests in? (type a phrase below) \n')
usr = input('What is the outlook username? \n')
pwd = input('What is the outlook password? \n')

url = 'https://mail.yourwaytransport.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yourwaytransport.com%2fowa%2f'

title = input('What is the title of your email?')

body = input('What is the body of your email? (input (backslash) + n instead return. \n')


driver = webdriver.Chrome()
driver.get(url)
print('opened outlook')
time.sleep(3)

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


def message_sender(recipient):
    dropdown = driver.find_element_by_xpath("//a[@id='newmsgcd']")
    time.sleep(2)
    dropdown.click()
    time.sleep(2)
    message_selection = driver.find_element_by_xpath("//a[@id='newmsg']")
    time.sleep(2)
    message_selection.click()
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


home = 'https://mail.yourwaytransport.com/owa/'

# print estimated time
et = num_clients * 39
minutes_raw = et / 60
minutes = math.trunc(minutes_raw)
seconds = et - (minutes * 60)
print('It will take ' + str(minutes) + ' minutes and ' + str(seconds) + ' seconds \
to send these emails.')

for client in email_list:
    message_sender(client)
    driver.get(home)
    time.sleep(5)
    print('sent to ' + str(client))

driver.close()
print('Done!')
