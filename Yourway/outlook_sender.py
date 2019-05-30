from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas

name = 'emails.csv'

data = pandas.read_csv(name)
email_list = data.email

# key_phrase = input('What category would you like to make requests in? (type a phrase below) \n')
usr = input('Enter your outlook username below. \n')
pwd = input('Enter your outlook password below. \n')

url = 'https://mail.yourwaytransport.com/owa/auth/logon.aspx?replaceCurrent=1&url=https%3a%2f%2fmail.yourwaytransport.com%2fowa%2f'

title = 'Premium Courier and Clinical Packaging'

body = 'New meeting requested \n\
I would like to introduce you to Yourway, the only true premium courier and clinical packager all in one company. We offer door to door service of any temp control shipment globally with now our own global GMP depot network with primary and secondary packaging, including short and long term storage of 15-25C, 2-8C, -20C and -80C and -180C and distribution. \n\
Main facility headquartered in Allentown, Pennsylvania, we also operate 21 other strategically-located GMP depots worldwide. Yourway is a premium courier of time- and temperature-sensitive clinical materials, and offers integrated clinical packaging, storage, and other specialty services. \n\
It would be a pleasure to formally introduce myself and tell you more, so I invite you to meet at BIO International, booth #4209. Do you have a good day/time? Or we could schedule a face-to-face that fits your schedule in the Partnering Forum? \n\n\ '


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
    dropdown.click()
    time.sleep(1)
    message_selection = driver.find_element_by_xpath("//a[@id='newmsg']")
    message_selection.click()
    time.sleep(1)
    window_before = driver.window_handles[0]
    window_after = driver.window_handles[1]
    driver.switch_to_window(window_after)
    time.sleep(3)
    to_box = driver.find_element_by_xpath("//div[@id='divTo']")
    to_box.send_keys(recipient)
    time.sleep(5)
    subject_box = driver.find_element_by_xpath("//input[@id='txtSubj']")
    subject_box.send_keys(title)
    time.sleep(5)
    body_box = driver.find_element_by_xpath("//iframe[@id='ifBdy']")
    body_box.send_keys(body)
    time.sleep(10)
    send_button = driver.find_element_by_xpath("//div[@id='divToolbarButtonsend']")
    send_button.click()
    time.sleep(1)
    return


for client in email_list:
    message_sender(client)


