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
        refresh_token(profile)
    user_name = get_username(profile.access_token)
    my_subreddits = get_my_subreddits(profile.access_token)

    return render(request, 'subs/my_subreddits.html', {'user_name': user_name, 'my_subreddits': my_subreddits})

def index_render(request):

    user = request.user
    profile = request.user.profile

    if request.method == 'POST':
        event_id = request.GET.get('id', '')
        event = Event.objects.filter(creator = user, event_id = event_id)[0]
        event.delete()

    checkEvents(user)

    #get all of the events which the user is a part of...
    events = Event.objects.filter(creator = user)
    current_events = []
    past_events = []
    for event in events:
        if event.end_date > timezone.now():
            current_events.append(event)
        else:
            past_events.append(event)

    return render(request, 'subs/index.html', {'current_events': current_events, 'past_events': past_events})
