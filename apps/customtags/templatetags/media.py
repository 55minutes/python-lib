from django.template import Library
register = Library()

def media_prefix():
    try:
        from django.conf import settings
    except ImportError:
        return ''
    return settings.MEDIA_URL
media_prefix = register.simple_tag(media_prefix)
