import praw

s = '/r/python'
s = s.replace("/r/","")


r = praw.Reddit('test by astonshane')
x = r.get_subreddit(s, fetch=True)

fullname = x.fullname.encode('utf-8')
print fullname
