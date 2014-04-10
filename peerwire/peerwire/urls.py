from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from django.contrib.auth import views as auth_views
from django.contrib import admin
admin.autodiscover()

sqs = SearchQuerySet().facet('status').facet('seeking').facet('level')

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/change/$',
        auth_views.password_change,
        name='password_change'),
    url(r'^a/change/done/$',
        auth_views.password_change_done,
        name='password_change_done'),
    url(r'^a/reset/$',
        auth_views.password_reset,
        name='password_reset'),
    url(r'^a/reset/done/$',
        auth_views.password_reset_done,
        name='password_reset_done'),
    url(r'^a/reset/complete/$',
        auth_views.password_reset_complete,
        name='password_reset_complete'),
    url(r'^a/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        name='password_reset_confirm'),
    # url(r'^a/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     auth_views.password_reset_confirm_uidb36,
    #     name='password_reset_confirm'),
    url(r'^a/', include('registration.backends.default.urls')),
    url(r'^s/$', FacetedSearchView(
        form_class=FacetedSearchForm,
        searchqueryset=sqs
        ), name='haystack_search'),
    url(r'^s/', include('haystack.urls')),
    url(r'^n/', include('news.urls', namespace='news')),
    url(r'^', include('projects.urls', namespace='projects')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
