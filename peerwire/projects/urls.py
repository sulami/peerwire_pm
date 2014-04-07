from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('projects.views',
    url(r'^$', 'index', name='index'),
    url(r'^p/(\d+)/$', 'projectpage', name='projectpage'),
    url(r'^u/(\d+)/$', 'profilepage', name='profilepage'),
    url(r'^p/(\d+)/e/$', 'edit_project', name='edit_project'),
    url(r'^p/s/$', 'start_project', name='start_project'),
    url(r'^p/(\d+)/s/$', 'startwork', name='startwork'),
    url(r'^p/(\d+)/f/$', 'finishwork', name='finishwork'),
    url(r'^e/p/$', 'edit_profile', name='edit_profile'),
    url(r'^e/l/$', 'edit_langs', name='edit_langs'),
    url(r'^e/s/$', 'edit_skills', name='edit_skills'),
    )
