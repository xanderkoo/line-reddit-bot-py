import praw

# def foo():
#     print("hi")

reddit = praw.Reddit(client_id='0YLur0TWpaPR0A',
                     client_secret='laA7ZB8Sbgx2ca9bg9fdmSmar3Q',
                     user_agent='xander',)

def get_top_n(sub_name, n):
    subreddit = reddit.subreddit(sub_name)
    return subreddit.hot(limit=n)
