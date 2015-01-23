import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.
class Event(models.Model):
    creator = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=200)
    subreddit = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    start_date = models.DateTimeField('start date')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        return self.title

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
