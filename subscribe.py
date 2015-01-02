import praw
import sys

def is_subscribed(subreddit):
    r = praw.Reddit(user_agent = "Alien Spoilers: v0.0.1")
    r.login()

    subs = r.get_my_subreddits()
    for sub in subs:
        if str(sub) == subreddit:
            return True
    return False


def subscribe(subreddit):
    r = praw.Reddit(user_agent = "Alien Spoilers: v0.0.1")
    try:
        r.login()
        try:
            r.get_subreddit(subreddit).subscribe()
            print "Subscribed to /r/", subreddit
        except:
            if is_subscribed(subreddit):
                print "ERROR: You are already subscribed to", subreddit
            else:
                print "Unexpected error:", sys.exc_info()[0]
            print "Could not subscribe to /r/", subreddit
    except:
        print "Unexpected error: Failed during login login: check username / password"

def unsubscribe(subreddit):
    r = praw.Reddit(user_agent = "Alien Spoilers: v0.0.1")
    try:
        r.login()
        try:
            r.get_subreddit(subreddit).unsubscribe()
            print "Unsubscribed from /r/", subreddit
        except:
            if not is_subscribed(subreddit):
                print "ERROR: You are not subscribed to ", subreddit
            else:
                print "Unexpected error:", sys.exc_info()[0]
            print "Could not unsubscribe from /r/", subreddit
    except:
        print "Unexpected error: Failed during login login: check username / password"
