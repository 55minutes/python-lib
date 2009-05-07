"""
Module for abstract serializer/unserializer base classes.
"""

from StringIO import StringIO

from django.conf import settings
from django.core.serializers.base import Serializer as DjangoBaseSerializer
from django.core.urlresolvers import get_callable
from django.db import models
from django.utils.encoding import smart_str, smart_unicode
from django.utils import datetime_safe

class Serializer(DjangoBaseSerializer):
    """
    Abstract serializer base class.
    """

    # Indicates if the implemented serializer is only available for
    # internal Django use.
    internal_use_only = False

    def serialize(self, queryset, **options):
        """
        Serialize a queryset of a single Model type.
        """
        self.queryset = queryset
        self.options = options
        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.converters = options.get('converters',
                                      settings.SERIALIZATION_CONVERTERS)

        self.fields_lookup()
        self.start_serialization()
        for obj in queryset:
            self.start_object(obj)
            for field in [f for f in obj._meta.fields if self.include_field(f)]:
                if field.rel is None:
                    self.handle_field(obj, field)
                else:
                    self.handle_fk_field(obj, field)
            for field in [f for f in obj._meta.many_to_many if self.include_field(f)]:
                self.handle_m2m_field(obj, field)
            for field in [f for f in self.queryset.query.extra if self.include_field(f)]:
                self.handle_extra(obj, field)
            for field in [f for f in self.queryset.query.aggregates if self.include_field(f)]:
                self.handle_aggregate(obj, field)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()

    def fields_lookup(self):
        self.fields = []
        model = self.queryset.model
        for field in [f for f in model._meta.fields if self.include_field(f)]:
            if field.rel is None:
                self.fields.append(field.attname)
            else:
                self.fields.append(field.attname[:-3])
        for field in [f for f in model._meta.many_to_many if self.include_field(f)]:
            self.fields.append(field.attname)
        for field in [f for f in self.queryset.query.extra if self.include_field(f)]:
            self.fields.append(field)
        for field in [f for f in self.queryset.query.aggregates if self.include_field(f)]:
            self.fields.append(field)

    def get_string_value(self, value):
        """
        Convert a Python type to a string.
        Fallback to Django smart_unicode if no converter is specified.
        """
        for k, v in self.converters.iteritems():
            if type(value) == k:
                value = get_callable(v)(value)
        return smart_unicode(value)

    def select_check(self, field, name):
        if self.selected_fields and name in self.selected_fields:
            return True
        if not self.selected_fields and field.serialize:
            return True
        return False

    def include_field(self, field):
        if issubclass(field.__class__, models.ManyToManyField):
            return self.select_check(field, field.attname)
        if issubclass(field.__class__, models.Field):
            if field.rel is None:
                return self.select_check(field, field.attname)
            else:
                return self.select_check(field, field.attname[:-3])
        if not self.selected_fields:
            return True
        if self.selected_fields and field in self.selected_fields:
            return True
        return False
