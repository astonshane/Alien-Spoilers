from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from uuid import uuid4
from django.contrib.auth.models import User
from subs.models import UserProfile, Event
from django.utils import timezone
import datetime
import urllib
import requests
from subreddit import Subreddit
import sys
import os

scriptpath = "subs/"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))
from oauthHelpers import *


def my_subreddits_render(request):
    profile = request.user.profile

    if(timezone.now() >= profile.token_expiry):
        refresh_token(request)
    user_name = get_username(profile.access_token)
    my_subreddits = get_my_subreddits(profile.access_token)

    return render(request, 'subs/my_subreddits.html', {'user_name': user_name, 'my_subreddits': my_subreddits})

def index_render(request):
    user = request.user
    profile = request.user.profile

    #get all of the events which the user is a part of...
    events = Event.objects.filter(creator = user)

    return render(request, 'subs/index.html', {'events': events})
