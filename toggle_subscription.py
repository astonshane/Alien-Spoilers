import praw
import sys


try:
    r = praw.Reddit(user_agent = "astonshane - test praw")
    r.login()
    subs = r.get_my_subreddits()

    found = False

    for sub in subs:
        s = str(sub)
        if s.lower() == "python":
            found = True

    if found:
        r.get_subreddit('python').unsubscribe()
        print "unsubscribing..."
    else:
        r.get_subreddit('python').subscribe()
        print "subscribing..."


except:
    print "Unexpected error:", sys.exc_info()[0]
