from django.conf.urls import patterns, include, url

from help import views

urlpatterns = patterns('help.views',
    url(r'^$', 'index', name='index'),
    url(r'^md/$', 'markdown', name='markdown'),
    url(r'^p/$', 'projects', name='projects'),
    )
