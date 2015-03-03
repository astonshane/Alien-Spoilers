import praw

r = praw.Reddit('test by astonshane')
x = r.get_subreddit('python', fetch=True)

fullname = x.fullname.encode('utf-8')
print fullname
