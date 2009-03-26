from django.conf.urls.defaults import include

def append_slash(x):
    if not x.endswith('/'):
        x += '/'
    return x

class Application(object):
    def __init__(self, url, url_include, version=None):
        self.url = url
        self.include = include(url_include)
        self.version = version
        self.regex = r'^%s' %append_slash(self.url)