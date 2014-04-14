from django.conf.urls import patterns, include, url

from projects import views

urlpatterns = patterns('projects.views',
    url(r'^$', 'index', name='index'),
    url(r'^p/(\d+)/$', 'projectpage', name='projectpage'),
    url(r'^u/(\d+)/$', 'profilepage', name='profilepage'),
    url(r'^p/(\d+)/e/$', 'edit_project', name='edit_project'),
    url(r'^p/(\d+)/e/u/$', 'manage_users', name='manage_users'),
    url(r'^p/(\d+)/e/u/(\d+)/$', 'manage_users', name='manage_users'),
    url(r'^p/(\d+)/e/o/$', 'add_owner', name='add_owner'),
    url(r'^p/(\d+)/e/r/$', 'owner_resign', name='owner_resign'),
    url(r'^p/s/$', 'start_project', name='start_project'),
    url(r'^p/(\d+)/p/$', 'start_project', name='start_project'),
    url(r'^p/(\d+)/d/$', 'delete_project', name='delete_project'),
    url(r'^p/(\d+)/d/t/$', 'delete_timer', name='delete_timer'),
    url(r'^p/(\d+)/d/c/$', 'delete_confirm', name='delete_confirm'),
    url(r'^p/(\d+)/w/$', 'startwork', name='startwork'),
    url(r'^p/(\d+)/f/$', 'finishwork', name='finishwork'),
    url(r'^e/p/$', 'edit_profile', name='edit_profile'),
    url(r'^e/l/$', 'edit_langs', name='edit_langs'),
    url(r'^e/s/$', 'edit_skills', name='edit_skills'),
    url(r'^about/$', 'about_us', name='about_us'),
    url(r'^contact/$', 'contact', name='contact'),
    )
