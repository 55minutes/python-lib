#!/usr/local/bin/python

import sys, os

home = '/hsphere/local/home/fiftyfiv'

sys.path.append(os.path.join( home, 'django/django_src'))
sys.path.append(os.path.join( home, 'django/projects'))
sys.path.append(os.path.join( home, 'lib/python/'))

from flup.server.fcgi_fork import WSGIServer
from django.core.handlers.wsgi import WSGIHandler

def runDjango(setting='', max_spare=1, max_children=1):
    os.environ['DJANGO_SETTINGS_MODULE'] = setting
    WSGIServer(WSGIHandler(),
            maxSpare=max_spare,
            maxChildren=max_children).run()

if __name__ == '__main__':
    runDjango('project.settings', 1, 1)
