import praw
from praw.exceptions import APIException
import pandas as pd
import json
import datetime
import time
import emailer

# read login information
name = 'reddit_login_info.csv'
login_info = pd.read_csv(name, header=0)

# read bot information
with open('reddit_games_info.txt') as json_file:
    game_info = json.load(json_file)

# get keyword, winphrase, message, and max_winners information
keyword = game_info['keyword']
message = game_info['message']
winphrase = game_info['winphrase']
winner_subject = game_info['winner_subject']
winner_message = game_info['winner_message']
max_winners = game_info['max_winners']
game_over_message = game_info['game_over_message']

# log in to reddit
reddit = praw.Reddit(client_id=login_info.clientid[0],
                     client_secret=login_info.secret[0], password=login_info.password[0],
                     user_agent=login_info.user_agent[0], username=login_info.username[0])

# set an api postcall limit
post_call_limit = game_info['max_calls']

date_start = str(datetime.datetime.today())

# create a mega list of posts to be turned into a dataframe
mega_list = []


def subreddit_post_scraper(post_call_limit, date_start, sent_list):
    # dissect start date
    date_start_year = int(date_start[:4])
    date_start_month = int(date_start[5:7])
    date_start_day = int(date_start[8:10]) - 1
    subreddit = reddit.subreddit('all').search(keyword, sort='new', limit=int(post_call_limit))  # not using stream because this will search by keyword better

    # find all of the posts in the subreddit
    post_list = []
    for submission in subreddit:
        # filter out all submissions before the desired date
        publish_date = str(datetime.datetime.utcfromtimestamp(submission.created_utc))
        if int(publish_date[:4]) < date_start_year:
            break
        if (int(publish_date[:4]) == date_start_year) and (int(publish_date[5:7]) < date_start_month):
            break
        if (int(publish_date[:4]) == date_start_year) and (int(publish_date[5:7]) == date_start_month) and (int(publish_date[8:10]) < date_start_day):
            break
        if submission.id in sent_list:
            break
        if submission not in post_list:
            post_list.append(submission)

    # get information for each submission
    for post in post_list:
        individual_cell = [post.title, post.selftext, post.id, datetime.datetime.utcfromtimestamp(post.created_utc)]
        if individual_cell not in mega_list:
            mega_list.append(individual_cell)
    return


# create a list of posts with messages that have already been sent (use post ids)
sent_list = []

# create a dictionary of {post ids : comment ids}
response_dict = {}

# create a dictionary to map the contenders author ; reply time
contenders = {}

# create a winners variable
winners = 0

# create a function to send a response to posts


def post_responder(post_id):
    submission = reddit.submission(post_id)
    submission.reply(message)
    sent_list.append(post_id)

    # let some time pass for reddit to update comment
    time.sleep(10)

    # get the comment id
    submission = reddit.submission(post_id)
    for comment in submission.comments:
        if str(comment.author).lower() in str(login_info.username[0]).lower():
            response_dict[post_id] = comment.id
    return


def comment_locator(post_id):
    global winners
    submission = reddit.submission(post_id)
    for comment in submission.comments:
        if comment.id == response_dict[post_id]:
            for reply in comment.replies:
                if winphrase in str(reply.body):
                    contenders[reply.author] = str(datetime.datetime.utcfromtimestamp(reply.created_utc))[-8:]  # keeps people from submitting multiple times and benefiting
                    winners += 1


# create a function to start the game

def game_on():

    # scrape reddit --> will be changed to intervals
    subreddit_post_scraper(post_call_limit, date_start, sent_list)

    # respond to new posts
    for submission in mega_list:
        post_id = submission[2]
        if post_id not in sent_list:
            if (keyword in submission[0]) or (keyword in submission[1]):
                post_responder(post_id)
    # locate comment thread
    for post_id in sent_list:
        comment_locator(post_id)

# create a function to end the competition


def end_comp(dict_pc):
    global game_over_message
    for post_id in dict_pc:
        submission = reddit.submission(post_id)
    for comment in submission.comments:
        if comment.id == response_dict[post_id]:
            try:
                comment.reply(game_over_message)
            except APIException:
                time.sleep(10)
                comment.reply(game_over_message)
    return


# create winners and runner ups into lists and strings for sending messages
winner_list = []
winner_string = ''
runner_up_list = []
runner_up_string = ''
winning_times = []


# create a function to find the earliest time

def find_lowest_time(time_list):
    lowest_hr = '23'
    lowest_min = '59'
    lowest_sec = '59'
    for reply_time in times:
        if int(reply_time[:2]) < int(lowest_hr):
            lowest_hr = reply_time[-8:-6]
        if (int(reply_time[:2]) == int(lowest_hr)) and (int(reply_time[-5:-3]) < int(lowest_min)):
            lowest_min = reply_time[-5:-3]
        if (int(reply_time[:2]) == int(lowest_hr)) and (int(reply_time[-5:-3]) == int(lowest_min)) and (int(reply_time[-2:]) < int(lowest_sec)):
            lowest_sec = reply_time[-2:]
    winning_time = lowest_hr + ':' + lowest_min + ':' + lowest_sec
    print(times)
    print(winning_time)
    times.remove(winning_time)
    return winning_time


# create a sending function

def pm_sender(recipient, subject, body):
    # send message
    reddit.redditor(recipient).message(subject, body)
    print('Winning notification sent to ' + str(recipient))
    return


# do it every second

while True:
    try:
        game_on()
    except TypeError:
        time.sleep(1)
    except APIException:
        time.sleep(10)
    if winners >= max_winners:
        break
    time.sleep(1)

# sort into winner and runner up lists
times = []
for contender in contenders:
    times.append(str(contenders[contender]))


# end competition by replying to all comments that the competition is over
end_comp(response_dict)

# get the winning times
for i in range(max_winners):
    winning_times.append(find_lowest_time(times))

# create a list of winners
# create an inverted dict for finding winning times
time_to_contender = dict(map(reversed, contenders.items()))
for t in winning_times:
    winner_list.append(str(time_to_contender[t]))
    winner_string += str(time_to_contender[t])
    winner_string += '; '

# create a list of runner ups (for future development)
for t in times:
    runner_up_list.append(str(time_to_contender[t]))
    runner_up_string += str(time_to_contender[t])
    runner_up_string += '\n'

# PM winners
for champ in winner_list:
    pm_sender(champ, winner_subject, winner_message)

# send email to client
subject = 'Reddit Game ' + date_start
body = ['The game has ended.', 'Here are the winners: ' + winner_string, 'Here are the runner ups: ' + runner_up_string]
emailer.send('naveen.ailawadi91@gmail.com', subject, body)
