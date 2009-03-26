import urlparse, os.path
from urllib import pathname2url
from django.conf import settings

from zip import *

def get_location(request=None):
    scheme, location, path, query, fragment = urlparse.urlsplit(settings.PROJECT_ROOT_URL)
    if request:
        location = request.META.get('HTTP_HOST', location)
    return location

def get_project_url(request=None):
    """\
    Based on settings params PROJECT_ROOT_URL
    Returns a tuple (url with FQDN, path only)
    Always returns WITH trailing "/"
    """
    scheme, location, path, query, fragment = urlparse.urlsplit(settings.PROJECT_ROOT_URL)
    if not path.endswith('/'): path+='/'
    location = get_location(request)
    full = urlparse.urlunsplit((scheme, location, path, query, fragment))
    return (full, path)

def get_app_url(request=None, app_key=None):
    """
    Based on settings params PROJECT_ROOT_URL and APPLICATIONS
    Returns a tuple (url with FQDN, path only)
    Always returns WITH trailing "/"
    app_key refers to the dictionary key in settings.APPLICATIONS
    """
    pru = get_project_url(request)[0]
    if request:
        found = False
        for app in settings.APPLICATIONS.values():
            if not app.url.endswith('/'): app.url+='/'
            full = urlparse.urljoin(pru, app.url)
            scheme, location, path, query, fragment = urlparse.urlsplit(full)
            if request.path.startswith(path):
                found = True
                break
        if found:
            return (full, path)
        else:
            return get_project_url(request)
    elif app_key:
        try:
            app = settings.APPLICATIONS[app_key]
            if not app.url.endswith('/'): app.url+='/'
            full = urlparse.urljoin(pru, app.url)
            scheme, location, path, query, fragment = urlparse.urlsplit(full)
            return (full, path)
        except KeyError:
            return get_project_url()
    else:
        return get_project_url()

def get_app_version(request=None, app_key=None):
    if request:
        found = False
        for app in settings.APPLICATIONS.values():
            if app.url in request.path:
                found = True
                break
        if found:
            return app.version
    elif app_key:
        try:
            app = settings.APPLICATIONS[app_key]
            return app.version
        except:
            pass
    return None
    
def get_media_url(*args):
    """\
    Based on settings params MEDIA_URL
    Returns a URL with optional arguments attached.
    """
    media_url = str(pathname2url(os.path.join(settings.MEDIA_URL, *args)))
    if not media_url.endswith('/'): media_url+='/'
    return media_url

def get_choice_key_by_value(choices, value):
    for k, v in choices:
        if v == value:
            return k
    return None