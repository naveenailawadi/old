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
entry = input('Enter reddit search term: \n')

# set an api postcall limit
post_call_limit = input('What is the maximum number of posts that you would like to return? \n')

# set start date
date_start = input("What is the earliest date that you would like to start scraping at (e.g. 2000-12-25)? \n")


def subreddit_post_scraper(entry, post_call_limit, date_start):
    # dissect start date
    date_start_year = int(date_start[:4])
    date_start_month = int(date_start[5:7])
    date_start_day = int(date_start[8:]) - 1
    subreddit = reddit.subreddit('all').search(entry, limit=int(post_call_limit))
    # create a list of lists for each post and its information
    mega_list = []

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
        post_list.append(submission)

    # find all the comments in the post
    for post in post_list:
        individual_cell = [post.title, post.id, post.author, int(post.ups - post.downs), datetime.datetime.utcfromtimestamp(post.created_utc), post.selftext]
        comment_list = []
        for comment in post.comments:
            try:
                comment_list.append(str(comment.body + ' (replies: ' + str(len(comment.replies))) + ')')
            except AttributeError:
                continue
        individual_cell.append(comment_list)
        mega_list.append(individual_cell)
    return mega_list


def subreddit_comment_scraper(entry, post_call_limit, date_start):
    # dissect start date
    date_start_year = int(date_start[:4])
    date_start_month = int(date_start[5:7])
    date_start_day = int(date_start[8:]) - 1
    subreddit = reddit.subreddit('all').search(entry, limit=int(post_call_limit))
    # create a list of lists for each post and its information
    mega_list = []

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
        post_list.append(submission)

    # find all the comments in the post
    for post in post_list:
        for comment in post.comments:
            individual_cell = [post.title, post.id, post.author, int(post.ups - post.downs), datetime.datetime.utcfromtimestamp(post.created_utc), post.selftext]
            try:
                new_addition = [comment.body, comment.id, comment.author, comment.ups, len(comment.replies)]
                for addition in new_addition:
                    individual_cell.append(addition)
                mega_list.append(individual_cell[:11])
            except AttributeError:
                continue
    return mega_list


# post dataframe
subreddit_posts_scraped = subreddit_post_scraper(entry, post_call_limit, date_start)
df_posts = pd.DataFrame(subreddit_posts_scraped, columns=['Title', 'post_id', 'Author', 'Vote_Score', 'Date', 'Body', 'Comments'])
print('Post Dataframe:')
print(df_posts)

# comment dataframe
subreddit_comments_scraped = subreddit_comment_scraper(entry, post_call_limit, date_start)
df_comments = pd.DataFrame(subreddit_comments_scraped, columns=['Title', 'post_id', 'Author', 'Vote_Score', 'Date', 'Body', 'Comment', 'comment_id', 'comment_author', 'ups', 'replies'])
print('Comment Dataframe:')
print(df_comments)
