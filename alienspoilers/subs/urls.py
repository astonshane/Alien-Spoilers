from django.conf.urls import patterns, url

from subs import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^authorize_callback/$', views.user_authorize_callback, name='callback'),
    url(r'^my_subreddits/$', views.my_subreddits, name='my_subreddits'),
    url(r'^create_event/$', views.create_event, name='create_event'),
    url(r'^link_account/$', views.link_account, name='link_account'),
)
