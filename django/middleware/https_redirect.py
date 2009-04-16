__credit__ = "Based on http://www.djangosnippets.org/snippets/85/"

from django.conf import settings
from django.http import HttpResponsePermanentRedirect

__all__ = ('HttpsRedirect',)

SSL = 'SSL'

class HttpsRedirect(object):
    """
    Django middleware to redirect ``http`` and ``https`` traffic.

    The middleware uses the fact that in URLconfs you can pass additional
    view parameters directly at the url pattern definition. For URLs that
    require SSL, you can mark them as such::

        url(regex, view, {'SSL':True}, name=url_name)

    For URLs marked with ``SSL=True``, the middleware will force a redirect
    to ``https`` protocol. For URLs marked with ``SSL=False`` or not explicitly
    marked, the middleware will force a redirect to ``http`` protocol.

    The ``SSL`` keyword argument is stripped from the view keyword arguments
    before passing on to the next middleware or to the view.
    """
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
