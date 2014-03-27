from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

from django.contrib import admin
admin.autodiscover()

sqs = SearchQuerySet().facet('status').facet('seeking').facet('level')

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^acc/', include('registration.backends.default.urls')),
    url(r'^s/$', FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs), name='haystack_search'),
    url(r'^s/', include('haystack.urls')),
    url(r'^n/', include('news.urls', namespace='news')),
    url(r'^', include('projects.urls', namespace='projects')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
