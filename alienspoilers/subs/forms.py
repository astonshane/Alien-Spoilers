from django import forms
from django.contrib.auth.models import User
from subs.models import UserProfile, Event
import datetime
from django.utils import timezone
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ()


class CreateEventForm(forms.ModelForm):

    #start_date = forms.DateTimeField(widget=forms.DateTimeInput(), initial=timezone.now())
    #end_date = forms.DateTimeField(widget=forms.DateTimeInput(), initial=timezone.now() + datetime.timedelta(days=1))

    class Meta:
        model = Event
        fields = ['title', 'subreddit']
