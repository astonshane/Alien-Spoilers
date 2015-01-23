from django.conf.urls import patterns, url

from subs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index')
)
