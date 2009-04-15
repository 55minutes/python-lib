from urlparse import urlunparse

from django.http import HttpResponseRedirect

class HttpsRedirect(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(view_func, '_https_only', False) and not request.is_secure():
            url = urlunparse(('https', request.get_host(),
                              request.get_full_path(), '', '', ''))
            return HttpResponseRedirect(url)
        else:
            return

class HttpRedirect(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if view_func.__module__.startswith('django.contrib'):
            return
        if not getattr(view_func, '_https_only', False) and request.is_secure():
            url = urlunparse(('http', request.get_host(),
                              request.get_full_path(), '', '', ''))
            return HttpResponseRedirect(url)
        else:
            return

def https_only(view_func):
    setattr(view_func, '_https_only', True)
    return view_func
