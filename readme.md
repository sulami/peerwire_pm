Peerwire Project Management Platform
====================================

TODO
----

  * featured projects

Software Setup
--------------

  * Nginx
  * MySQL /w InnoDB
  * Elasticsearch (tested on 1.0.1)
  * Redis
  * Python (>= 2.7)
  * Python-pyelasticsearch (tested on 0.6.1)
  * Python-requests (tested on 2.2.1)
  * Python-markdown (tested on 2.4)
  * Python-pygments (tested on 1.6)
  * Python-pip (tested on 2.7.5)
    * libjpeg-devel
    * libz-devel
    * libfreetype-devel
  * Django (tested on 1.6.4)
  * Django-registration (tested on 0.9.3)
  * Django-haystack (tested on 2.1.0)
  * Django-cacheops (tested on 1.3.1)

Custom Fixes
------------

django core: /usr/lib/python2.7/site-packages/django/contrib/auth/models.py:

<<
    AbstractUser: email = blank=True

>>
    AbstractUser: email = unique=True

registration: /usr/lib/python2.7/site-packages/registration/forms.py:
(fix custom user model)

<<
    from django.contrib.auth.models import User

>>
    from django.contrib.auth import get_user_model
    User = get_user_model()

registration: /usr/lib/python2.7/site-packages/registration/auth_urls.py:
(fix Django 1.6 base64-encoding)

<<
    url(r'^password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',

>>
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',

registration: /usr/lib/python2.7/site-packages/registration/auth_urls.py:

>>
    29:
        from django.core.urlresolvers import reverse_lazy
    45:
        {'post_change_redirect': reverse_lazy('auth_password_change_done')},
    52:
        {'post_reset_redirect': reverse_lazy('auth_password_reset_done')},
    56:
        {'post_reset_redirect': reverse_lazy('auth_password_reset_complete')},

Cronjobs
--------

  * Recalc Values | every 24h
  * Delete orphan files | as needed
  * Clean projects | as needed, daily
  * Clean users | daily
  * Generate Stats | as needed

[//]: # vim:filetype=markdown

