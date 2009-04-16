__credit__ = "Based on http://www.djangosnippets.org/snippets/85/"

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

__all__ = ('HttpsRedirect',)

SSL = 'SSL'

class HttpsRedirect(object):
    def process_view(self, request, view_func, view_args, view_kwargs):
        secure = view_kwargs.pop(SSL, False)
        if secure != self.is_secure(request) and self.has_ssl():
            protocol = secure and "https" or "http"
            return self.redirect(protocol, request)

    def has_ssl(self):
        return getattr(settings, 'SSL_ENABLED', False)

    def is_secure(self, request):
        #Handle the Webfaction case until this gets resolved in the request.is_secure()
        if 'HTTP_X_FORWARDED_SSL' in request.META:
            return request.META['HTTP_X_FORWARDED_SSL'] == 'on'
        else:
            return request.is_secure()

    def redirect(self, protocol, request):
        url = "%s://%s%s" % (
            protocol, request.get_host(), request.get_full_path())
        return HttpResponsePermanentRedirect(url)
