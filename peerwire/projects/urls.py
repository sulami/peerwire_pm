from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('projects.views',
    url(r'^$', 'index', name='index'),
    url(r'^p/(\d+)/$', 'projectpage', name='projectpage'),
    url(r'^u/(\d+)/$', 'profilepage', name='profilepage'),
    url(r'^p/(\d+)/e/$', 'edit_project', name='edit_project'),
    url(r'^u/e/$', 'edit_profile', name='edit_profile'),
    )
