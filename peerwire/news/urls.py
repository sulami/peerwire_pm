from django.conf.urls import patterns, include, url

from news import views
from news.feeds import NewsFeed

urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(\d+)/$', 'newspage', name='newspage'),
    url(r'^f/$', NewsFeed(), name='newsfeed'),
    )
