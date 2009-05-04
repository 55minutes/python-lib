from django.contrib.admin import site
from django.contrib.admin.sites import NotRegistered
from django.contrib import databrowse
from django.contrib.databrowse.sites import NotRegistered as DBNotRegistered

def register(model_or_iterable, admin_class=None, **options):
    try:
        site.unregister(model_or_iterable)
    except NotRegistered:
        pass
    site.register(model_or_iterable, admin_class, **options)

def register_with_databrowse(model_or_iterable, admin_class=None, databrowse_class=None, **options):
    register(model_or_iterable, admin_class, **options)
    try:
        databrowse.site.unregister(model_or_iterable)
    except DBNotRegistered:
        pass
    databrowse.site.register(model_or_iterable, databrowse_class, **options)
