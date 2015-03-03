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
    #start_date = forms.DateTimeField(widget=forms.SplitDateTimeWidget(), initial=datetime.now())
    #end_date = forms.DateTimeField(widget=AdminDateWidget)
    #start_date = forms.DateField(widget=widgets.AdminDateWidget)
    #end_date = forms.DateField(widget=widgets.AdminDateWidget)
    #title = forms.CharField()
    #subreddit = forms.CharField()

    start_date = forms.DateTimeField(widget=forms.DateTimeInput(), initial=timezone.now())
    end_date = forms.DateTimeField(widget=forms.DateTimeInput(), initial=timezone.now() + datetime.timedelta(days=1))

    class Meta:
        model = Event
        fields = ['title', 'subreddit', 'start_date', 'end_date']


        '''creator = User

        title = forms.CharField('Event Title:')

        start_date = forms.DateTimeField(initial=datetime.now())
        end_date = forms.DateTimeField(initial=datetime.now())'''
