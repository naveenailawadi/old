from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas

name = 'emails.csv'

data = pandas.read_csv(name)
email_list = data.email

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
    time.sleep(1)
    dropdown.click()
    time.sleep(1)
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
    time.sleep(10)
    send_button = driver.find_element_by_xpath("//div[@id='divToolbarButtonsend']")
    send_button.click()
    time.sleep(3)
    driver.switch_to_window(window_before)
    time.sleep(5)
    return


home = 'https://mail.yourwaytransport.com/owa/'

for client in email_list:
    message_sender(client)
    driver.get(home)
    time.sleep(5)
    print('sent to ' + str(client))

driver.close()
print('Done!')
