from django.contrib import admin
from subs.models import Event
from subs.models import UserProfile

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'subreddit', 'subreddit_fullname', 'start_date', 'end_date', 'pub_date', 'repeat', 'repeat_type', 'was_published_recently')

# Register your models here.
admin.site.register(Event, EventAdmin)
admin.site.register(UserProfile)
