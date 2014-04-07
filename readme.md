Peerwire Project Management Platform
====================================

TODO
----

  * search facets for languages
  * credit system
  * featured projects
  * premium account preparations

Software Setup
--------------

  * Nginx
  * MySQL /w InnoDB
  * Elasticsearch (tested on 1.0.1)
  * Python (>= 2.7)
  * Python-pyelasticsearch (tested on 0.6.1)
  * Python-requests (tested on 2.2.1)
  * Django (tested on 1.6.4)
  * Django-registration (tested on 0.9.3)
  * Django-haystack (tested on 2.1.0)
  * Django-orphaned (tested on 0.3)

URL overview
------------

/       - index page
/u/1/   - user page 1
/p/1/   - project page 1
/s/     - haystack search stack
/n/     - news index
/n/1/   - news post 1
/a/     - account management by django-registration

/static/    - static files
/media/     - media files

[//]: # vim:filetype=markdown

