"""
A Python "serializer". Doesn't do much serializing per se -- just converts to
and from basic Python data types (lists, dicts, strings, etc.). Useful as a basis for
other serializers.
"""

from django.core.serializers.python import Serializer as DjangoPythonSerializer
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.encoding import smart_unicode, is_protected_type

import base

class Serializer(base.Serializer, DjangoPythonSerializer):
    """
    Serializes a QuerySet to into a list self.objects.
    Each object is in the form of a Python dictionary:
    {
    'model': app_label.model_name,
    'pk': obj.pk,
    'fields' : {
        'field1_name':field1_value,
        'field2_name':field2_value,
        ...
        }
    }
    """
    def start_object(self, obj):
        self._current = SortedDict()
    
    def handle_extra(self, obj, field):
        self._current[field] = getattr(obj, field)
    handle_aggregate = handle_extra
