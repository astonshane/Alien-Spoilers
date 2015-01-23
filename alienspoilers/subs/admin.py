from django.contrib import admin
from subs.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'subreddit', 'start_date', 'end_date', 'pub_date', 'was_published_recently')

# Register your models here.
admin.site.register(Event, EventAdmin)
