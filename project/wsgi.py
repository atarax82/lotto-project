"""
WSGI config for lotto project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

import sys
sys.path.insert(1, os.path.normpath(os.path.join(os.path.dirname(__file__), '../')))

# monitor
from project import monitor
monitor.start(interval=1.0)
monitor.track(os.path.join(os.path.dirname(__file__), 'site.cf'))

application = get_wsgi_application()
