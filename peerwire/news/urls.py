from django.conf.urls import patterns, include, url

from news import views

urlpatterns = patterns('news.views',
    url(r'^$', 'index', name='index'),
    url(r'^(\d+)/$', 'newspage', name='newspage'),
    )
