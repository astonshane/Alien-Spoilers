class Subreddit:
    def __init__(self, name, fullname):
        self.name = name
        self.fullname = fullname
        self.url = "http://www.reddit.com" + name

    def __str__(self):
        print self.name
