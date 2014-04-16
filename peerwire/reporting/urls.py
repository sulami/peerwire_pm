from django.conf.urls import patterns, include, url

from reporting import views

urlpatterns = patterns('reporting.views',
    url(r'^p/(\d+)/$', 'r_project', name='r_project'),
    url(r'^u/(\d+)/$', 'r_user', name='r_user'),
)

