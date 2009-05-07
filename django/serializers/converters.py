from django.utils import datetime_safe

def none(value):
    return u''

def date(value):
    return datetime_safe.new_date(value).strftime("%Y-%m-%d")

def datetime(value):
    return datetime_safe.new_datetime(value).strftime('%Y-%m-%d %H:%M:%S')

def time(value):
    return value.strftime("%H:%M:%S")
