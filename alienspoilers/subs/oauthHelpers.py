from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subs.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.contrib.auth.models import User
from subs.models import UserProfile, Event
from django.utils import timezone
import datetime
import urllib
import requests
import ConfigParser
from subreddit import Subreddit

#parse the config file to get the oauth client id/secret
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
CLIENT_ID = Config.get("reddit", "oauth_client_id")
CLIENT_SECRET = Config.get("reddit", "ouath_client_secret")
REDIRECT_URI = Config.get("reddit", "oauth_redirect_uri")

def user_agent():
    '''
    reddit API clients should each have their own, unique user-agent
    Ideally, with contact info included.
    '''
    return "Alien Spoilers - astonshane@gmail.com - v0.0.2"

def base_headers():
    return {"User-Agent": user_agent()}

def make_authorization_url():
    # Generate a random string for the state parameter
    state = str(uuid4())
    print REDIRECT_URI
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "permanent",
              "scope": "identity,mysubreddits,subscribe"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

def get_initial_token(request, code):
    print "getting initial token"
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()

    #update the UserProfile data model with the new data
    profile = request.user.profile
    profile.access_token = token_json["access_token"]
    profile.refresh_token = token_json["refresh_token"]
    profile.reddit_linked = True
    profile.token_expiry = timezone.now() + datetime.timedelta(hours=1)
    profile.save()

    return token_json["access_token"]

def refresh_token(profile):
    print "refreshing token"
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "refresh_token",
                 "refresh_token": profile.refresh_token,
                 "redirect_uri": REDIRECT_URI}
    headers = base_headers()
    response = requests.post("https://ssl.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             headers=headers,
                             data=post_data)
    token_json = response.json()

    #update the UserProfile data model with the new data
    #profile = request.user.profile
    profile.access_token = token_json["access_token"]
    #profile.refresh_token = token_json["refresh_token"]
    profile.token_expiry = timezone.now() + datetime.timedelta(hours=1)
    profile.save()

    #return token_json["access_token"]


def get_username(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
    me_json = response.json()
    #print me_json
    return me_json['name']

def get_my_subreddits(access_token):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    response = requests.get("https://oauth.reddit.com/subreddits/mine/subscriber?limit=100", headers=headers)
    dump = response.json()

    #print my_subreddits

    data = dump['data']

    all_subreddits = data['children']

    #dictionary
    my_subreddits = []

    for subreddit in all_subreddits:
        data = subreddit['data']
        fullname = data['name']
        url = data['url']
        #                gets rid of the u' thing
        name = url.encode('utf-8')

        #print name, fullname

        sub = Subreddit(name, fullname)
        my_subreddits.append(sub)

    return my_subreddits

def unsubscribe(access_token, fullname):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    headers.update({"Content-Type": "application/json"})
    rqst = "https://oauth.reddit.com/api/subscribe?action=unsub&sr=" + fullname
    #print rqst
    response = requests.post(rqst, headers=headers)
    dump = response.json()
    #print dump

def subscribe(access_token, fullname):
    headers = base_headers()
    headers.update({"Authorization": "bearer " + access_token})
    headers.update({"Content-Type": "application/json"})
    rqst = "https://oauth.reddit.com/api/subscribe?action=sub&sr=" + fullname
    #print rqst
    response = requests.post(rqst, headers=headers)
    dump = response.json()
    #print dump

def checkEvents(user):
    #print "Checking Events"
    events = Event.objects.filter(creator = user)
    for event in events:
        current_time = timezone.now()
        if current_time > event.start_date and current_time < event.end_date:
            profile = user.profile
            if(timezone.now() >= profile.token_expiry):
                refresh_token(profile)

            access_token = profile.access_token
            fullname = event.subreddit_fullname
            my_subreddits = get_my_subreddits(access_token)
            found = False

            for subreddit in my_subreddits:
                if subreddit.fullname == fullname:
                    found = True
                    break

            if(found):
                #print "Unsubscribing from:", event.subreddit
                unsubscribe(access_token, fullname)
