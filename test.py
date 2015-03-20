import praw

s = '/r/sarah'
s = s.replace("/r/","")


r = praw.Reddit('test by astonshane')
x = ""
try:
    x = r.get_subreddit(s, fetch=True)
    print "succeeded"
except:
    print x, "failed"
#fullname = x.fullname.encode('utf-8')
#print fullname
