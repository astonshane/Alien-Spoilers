from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from subs.forms import UserForm, UserProfileForm, CreateEventForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.contrib.auth.models import User
from subs.models import UserProfile
from django.utils import timezone
import datetime
import urllib
import ConfigParser
from subreddit import Subreddit
from oauthHelpers import *

#parse the config file to get the oauth client id/secret
Config = ConfigParser.ConfigParser()
Config.read("config.ini")
CLIENT_ID = Config.get("reddit", "oauth_client_id")
CLIENT_SECRET = Config.get("reddit", "ouath_client_secret")
REDIRECT_URI = Config.get("reddit", "oauth_redirect_uri")

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

#not used?
@login_required
def link_account(request):
    authorize_url = make_authorization_url()
    return render(request, 'subs/link_account.html', {'authorize_url': authorize_url})

@login_required
def user_authorize_callback(request):

    error = request.GET.get('error', '')
    if error:
        return "Error: " + error

    state = request.GET.get('state', '')
    code = request.GET.get('code')

    get_initial_token(request, code)

    return index_render(request)

@login_required
def create_event(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    created = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        event_form = CreateEventForm(data=request.POST)

        # If the for is valid...
        if event_form.is_valid():
            # Save the user's form data to the database.
            event = event_form.save(commit=False)
            print event
            event.creator = request.user
            event.pub_date = timezone.now()
            print event
            event.save()

            # Update our variable to tell the template the event creation was successful.
            created = True

        # Invalid form?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print event_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        event_form = CreateEventForm()

    # Render the template depending on the context.
    return render(request,
            'subs/create_event.html',
            {'event_form': event_form, 'created': created} )
