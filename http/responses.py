from django.http import HttpResponseRedirect

__all__ = ('HttpResponseSeeOther',)

class HttpResponseSeeOther(HttpResponseRedirect):
    status_code = 303
