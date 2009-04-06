from django.contrib.admin import site
from django.contrib.admin.sites import NotRegistered

def register(model_or_iterable, admin_class=None, **options):
    try:
        site.unregister(model_or_iterable)
    except NotRegistered:
        pass
    site.register(model_or_iterable, admin_class=None, **options)
