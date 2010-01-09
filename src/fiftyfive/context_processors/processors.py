"""
Request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
DjangoContext.
"""

import urlparse
from fiftyfive.helpers.utils import *
from django.conf import settings

def install_url(request):
    """
    Returns context variables required by apps that use APP_RELATIVE_URL
    configuration parameter
    """

    cd = dict(
        project_full_url = get_project_url(request)[0],
        project_url = get_project_url(request)[1],
        app_full_url = get_app_url(request)[0],
        app_url = get_app_url(request)[1],
        media_url = settings.MEDIA_URL,
        media_root = settings.MEDIA_ROOT,
        )
    return cd

def install_settings(request):
    cd = dict(
        settings = settings
        )
    return cd

def install_version(request):
    cd = dict(
        app_version = get_app_version(request)
        )
    return cd
