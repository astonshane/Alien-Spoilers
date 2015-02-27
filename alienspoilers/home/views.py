from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subs.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.contrib.auth.models import User
from subs.models import UserProfile
from django.utils import timezone
import datetime
import urllib
import ConfigParser
import sys
import os

scriptpath = "subs/"

# Add the directory containing your module to the Python path (wants absolute paths)
sys.path.append(os.path.abspath(scriptpath))

# Do the import
from oauthHelpers import *

# Create your views here.

def index(request):
    if request.user.is_authenticated():
        #if user hasn't linked their reddit account yet, send them to a page to do that...
        profile = request.user.profile
        if profile.reddit_linked:
            return index_render(request)
        else:
            return render(request, 'subs/index.html', {'link_url': make_authorization_url()})
    else:
        return render(request, 'home/index.html')
    #return HttpResponse("Hello World. Homepage")
