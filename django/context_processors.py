import os, sys

from django.conf import settings
from fiftyfive.utils.svn_version import get_svn_revision

def svn_revision(request):
    "Returns context variable for SVN revision number."
    context_extras = {}
    settings_module = sys.modules[os.environ['DJANGO_SETTINGS_MODULE']]
    context_extras['svn_revision'] = get_svn_revision(
        os.path.split(settings_module.__file__)[0])
    return context_extras
