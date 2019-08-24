import csv

print('Follow the instructions below to input the necessary information into a csv for future reference.')


with open('reddit_login_info.csv', 'w') as file:
    # let w represent our file
    w = csv.writer(file)

    # write the header row
    w.writerow(['clientid', 'secret', 'password', 'user_agent', 'username'])
    clientid = input('What is your clientid? \n')
    secret = input('What is your secret key? \n')
    user_agent = 'useragentex'
    username = input('What is your username? \n')
    password = input('What is your password? \n')
    w.writerow([clientid, secret, password, user_agent, username])

print('Done. your data file has been created.')
