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

class Subreddit:
    def __init__(self, name, fullname):
        self.name = name
        self.fullname = fullname
        self.url = "http://www.reddit.com" + name

    def __str__(self):
        print self.name


#hacky hacky hacky. need to get this to work with built in PRAW config...
config = open("config.ini")
CLIENT_ID = config.readline().split()[1]
CLIENT_SECRET = config.readline().split()[1]
REDIRECT_URI = config.readline().split()[1]
config.close()
import requests
import requests.auth



# Create your views here.

@login_required
def index(request):
    #if user hasn't linked their reddit account yet, send them to a page to do that...
    profile = request.user.profile
    if profile.reddit_linked:
        return index_render(request)
    else:
        return render(request, 'subs/index.html', {'link_url': make_authorization_url()})

def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user


            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'subs/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )



def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/subs/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your AlienSpoilers account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return render(request,'subs/login.html', {'invalid':True})
            #return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'subs/login.html', {'invalid':False})




# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')


def user_agent():
    '''reddit API clients should each have their own, unique user-agent
    Ideally, with contact info included.

    e.g.,
    return "oauth2-sample-app by /u/%s" % your_reddit_username

    '''
    return "Alien Spoilers - astonshane@gmail.com - v0.0.2"

def base_headers():
    return {"User-Agent": user_agent()}

def make_authorization_url():
    # Generate a random string for the state parameter
    state = str(uuid4())
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "permanent",
              "scope": "identity,mysubreddits,subscribe"}
    url = "https://ssl.reddit.com/api/v1/authorize?" + urllib.urlencode(params)
    return url

@login_required
def link_account(request):

    authorize_url = make_authorization_url()

    return render(request, 'subs/link_account.html', {'authorize_url': authorize_url})


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

def refresh_token(request):
    print "refreshing token"
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "refresh_token",
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
    profile.token_expiry = timezone.now() + datetime.timedelta(hours=1)
    profile.save()

    return token_json["access_token"]

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

def index_render(request):
    profile = request.user.profile
    if(timezone.now() >= profile.token_expiry):
        refresh_token(request)

    user_name = get_username(profile.access_token)
    my_subreddits = get_my_subreddits(profile.access_token)

    return render(request, 'subs/index.html', {'user_name': user_name, 'my_subreddits': my_subreddits})

@login_required
def user_authorize_callback(request):

    error = request.GET.get('error', '')
    if error:
        return "Error: " + error

    state = request.GET.get('state', '')
    code = request.GET.get('code')

    get_initial_token(request, code)

    return index_render(request)
