import os, sys, site


site.addsitedir('/var/www/todo/env/lib/python2.7/site-packages')
sys.path.append('/var/www/todo/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'todo.settings'

import django.core.handlers.wsgi
from raven.contrib.django.middleware.wsgi import Sentry
application = Sentry(django.core.handlers.wsgi.WSGIHandler())