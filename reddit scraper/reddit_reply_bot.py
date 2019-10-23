'''
Recently, I found that I was spending way too much time on reddit looking for programming jobs.
As a result, I used my knowledge of the PRAW library to scrape subreddits for
certain keywords. Now, if any of the keywords apply, you can reach out to the subsequent
redditor.
'''


import praw
import pandas as pd
import datetime

# read login information
name = 'reddit_login_info.csv'
info_csv = pd.read_csv(name, header=0)

# log in to reddit
reddit = praw.Reddit(client_id=info_csv.clientid[0],
                     client_secret=info_csv.secret[0], password=info_csv.password[0],
                     user_agent=info_csv.user_agent[0], username=info_csv.username[0])


# enter and acces decided subreddit
entry = input('Which subreddit would you like to scrape? \n')

# set an api postcall limit
post_call_limit = input('What is the maximum number of posts that you would like to return? \n')

# set start date
date_start = input("What is the earliest date that you would like to start scraping at (e.g. 2000-12-25)? \n")


def subreddit_post_scraper(entry, post_call_limit, date_start):
    # dissect start date
    date_start_year = int(date_start[:4])
    date_start_month = int(date_start[5:7])
    date_start_day = int(date_start[8:]) - 1
    subreddit = reddit.subreddit(entry)
    # create a list of lists for each post and its information
    mega_list = []

    # find all of the posts in the subreddit
    post_list = []
    for submission in subreddit.new(limit=int(post_call_limit)):
        # filter out all submissions before the desired date
        publish_date = str(datetime.datetime.utcfromtimestamp(submission.created_utc))
        if int(publish_date[:4]) < date_start_year:
            break
        if (int(publish_date[:4]) == date_start_year) and (int(publish_date[5:7]) < date_start_month):
            break
        if (int(publish_date[:4]) == date_start_year) and (int(publish_date[5:7]) == date_start_month) and (int(publish_date[8:10]) < date_start_day):
            break
        post_list.append(submission)

    # find all the comments in the post
    for post in post_list:
        individual_cell = [post.title, post.id, post.author, datetime.datetime.utcfromtimestamp(post.created_utc), post.selftext]
        mega_list.append(individual_cell)
    return mega_list


# post dataframe
subreddit_posts_scraped = subreddit_post_scraper(entry, post_call_limit, date_start)
df_posts = pd.DataFrame(subreddit_posts_scraped, columns=['Title', 'post_id', 'Author', 'Date', 'Body'])
# print('Post Dataframe:')
# print(df_posts)


# create a function that extracts authors from the dataframe (by keyword) and exports them as a list

def contact_finder():
    # find keyword entries
    keywords = []
    keywords.append(input('Enter the first keyword that you want to scrape for: \n'))

    while True:
        new_keyword = input('Enter a keyword that you want to add below: \n\
    otherwise, write "I am done") \n')
        # create a breaking method
        if "i am done" in new_keyword.lower():
            break
        elif new_keyword in keywords:
            print('You have already selected that article.')
        else:
            keywords.append(new_keyword)

    found_titles = []
    print('Here are the titles that match your criteria:')
    for title in df_posts['Title']:
        for keyword in keywords:
            if keyword.lower() in title.lower():
                try:
                    print(title)
                    found_titles.append(title)
                except UnicodeEncodeError:
                    pass

    selected_titles = []
    count = 0
    while count != 1:
        response = input('Paste the titles that you want to reply to below: \n\
    otherwise, write "I am done") \n')
        # create a breaking method
        if "i am done" in response.lower():
            count = 1
        elif response in found_titles:
            selected_titles.append(response)
        # scan to check errors
        elif response in selected_titles:
            print('You have already selected that post.')
        else:
            print('Input Error. Try again. \n\n')
    print("title selection finished")

    # create a list of redditors to reach out to
    redditor_list = []
    print('redditor list created')

    # create a link between the titles and the reddit usernames
    for title in selected_titles:
        print('scanning title \n\n')
        for cell in subreddit_posts_scraped:
            if title.lower() in cell[0].lower():
                print(cell[0] + ' - ' + str(cell[2]))
                try:
                    print(cell[4])
                except UnicodeEncodeError:
                    continue
                while True:
                    yes_or_no = input('Do you want to reach out to this author (yes or no)? \n')
                    if 'yes' in yes_or_no.lower():
                        redditor_list.append(cell[2])
                        break
                    elif 'no' in yes_or_no.lower():
                        break
                    else:
                        print('ResponseError: Try again.')
                        continue
    return redditor_list


# list with small cells of 3 attributes:
final_send_list = []

# create a function to link each recipient with a subject and message


def message_structure(recipient):
    # set information for mass sender

    pm_subject = input('Please paste the pm subject for ' + str(recipient) + ' below: \n')
    pm_text = input('Please paste the pm text below: \n')
    minicell = [recipient, pm_subject, pm_text]
    final_send_list.append(minicell)
    return


# create a function for sending each message (this will later be used for multithreading
def pm_sender(recipient, subject, body):
    # send message
    reddit.redditor(recipient).message(subject, body)
    print('message sent to ' + str(recipient))
    return


# run the necessary functions to set up
redditor_list = contact_finder()

# write messages
for contact in redditor_list:
    message_structure(contact)

# iterate over all of the selections to finish
for block in final_send_list:
    recipient = str(block[0])
    subject = str(block[1])
    body = str(block[2])
    pm_sender(recipient, subject, body)
