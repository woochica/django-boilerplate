#!/usr/bin/python
import os
import sys
import site

sys.path.append('/usr/local/www/webroot/DOMAIN/staging/site/')
sys.path.append('/usr/local/www/webroot/DOMAIN/staging/site/site-packages')
site.addsitedir('/usr/local/www/webroot/DOMAIN/staging/virtualenv/lib/python2.6/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'PROJECT.settings'
os.environ['PYTHON_EGG_CACHE'] = '/tmp'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
