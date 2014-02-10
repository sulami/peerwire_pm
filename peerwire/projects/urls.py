from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('projects.views',
    url(r'^$', 'index', name='index'),
    )
