"""
WSGI config for fl_ask project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fl_ask.settings")

application = get_wsgi_application()
"""def application(env,start_response):
	start_response('200 OK', [('Content-Type', 'text/html')])
	return ["Hello World!"]"""
