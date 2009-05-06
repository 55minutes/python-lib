"""
Based on http://code.djangoproject.com/attachment/ticket/5253/csv_serializer.2.patch?format=raw
"""
import os, re
try:
    from cStringio import StringIO
except:
    from StringIO import StringIO

from django.core.serializers import base
from django.db import models
from django.utils.encoding import smart_unicode

from fiftyfive.utils import csv_ as csv

spaces_re = re.compile('^\s+$')

class Serializer(base.Serializer):
    "Serialize a QuerySet to csv"

    def serialize(self, queryset, **options):
        """
        Serialize a queryset.
        """
        self.options = options

        self.stream = options.get("stream", StringIO())
        self.selected_fields = options.get("fields")
        self.extra = queryset.query.extra.keys()
        self.aggregates = queryset.query.aggregates.keys()

        self.start_serialization()
        for obj in queryset:
            self.start_object(obj)
            for field in obj._meta.local_fields:
                if field.serialize:
                    if field.rel is None:
                        if self.selected_fields is None or field.attname in self.selected_fields:
                            self.handle_field(obj, field)
                    else:
                        if self.selected_fields is None or field.attname[:-3] in self.selected_fields:
                            self.handle_fk_field(obj, field)
            for field in obj._meta.many_to_many:
                if field.serialize:
                    if self.selected_fields is None or field.attname in self.selected_fields:
                        self.handle_m2m_field(obj, field)
            for field in self.extra:
                self.handle_extra(obj, field)
            for field in self.aggregates:
                self.handle_aggregate(obj, field)
            self.end_object(obj)
        self.end_serialization()
        return self.getvalue()

    def start_serialization(self):
        self.last_model = None
        # By default, csv module uses '\r\n' as lineterminator
        self.output = csv.UnicodeWriter(self.stream, lineterminator=os.linesep)

    def start_object(self, obj):
        if not hasattr(obj, "_meta"):
            raise base.SerializationError("Non-model object (%s) encountered during serialization" % type(obj))
        if self.last_model != obj.__class__:
            self.last_model = obj.__class__
            meta = obj._meta
            fields = self.selected_fields
            if fields:
                fields = list(fields)
            else:
                fields = [f.name for f in meta.fields+meta.many_to_many]
            if meta.pk.attname in fields:
                fields.remove(meta.pk.attname)
            header = ['%s:%s' % (meta, meta.pk.attname)]
            for field_name in fields:
                header.append(field_name)
            for field_name in self.extra:
                header.append(field_name)
            for field_name in self.aggregates:
                header.append(field_name)
            # Table separator is an empty row
            self.output.writerow([])
            self.output.writerow(header)
        self.row = [str(obj._get_pk_val())]

    def end_object(self, obj):
        self.output.writerow(self.row)

    def handle_field(self, obj, field):
        self.row.append(self.get_string_value(obj, field))

    def handle_extra(self, obj, field):
        self.row.append(smart_unicode(getattr(obj, field)))

    def handle_aggregate(self, obj, field):
        self.row.append(smart_unicode(getattr(obj, field)))

    def handle_fk_field(self, obj, field):
        related = getattr(obj, field.name)
        if related is None:
            repr = ''
        else:
            if field.rel.field_name == related._meta.pk.name:
                # relation via pk
                repr = str(related._get_pk_val())
            else:
                # relation via other field
                repr = str(getattr(related, field.rel.field_name))
        self.row.append(repr)

    def handle_m2m_field(self, obj, field):
        """Represented as a tuple of related ids, or empty string of there
        are no related objects"""
        related = [related._get_pk_val() for related in getattr(obj, field.name).iterator()]
        if related:
            self.row.append(str(related))
        else:
            self.row.append('')

    def get_string_value(self, obj, field):
        """
        None always becomes ''.  For string values prepend a leading
        space if the string contains only spaces so '' becomes ' ' and '
        ' becomes '  ', etc.  Other values are handled normally.
        """
        value = getattr(obj, field.name)
        if value is None:
            return ''
        elif is_string_field(field):
            if spaces_re.match(value):
                return ' ' + value
            else:
                return value
        else:
            return super(Serializer, self).get_string_value(obj, field)


class Deserializer(base.Deserializer):
    "Deserialize from csv"

    def __init__(self, stream_or_string, **options):
        super(Deserializer, self).__init__(stream_or_string, **options)
        self.next = self.__iter__().next

    def __iter__(self):
        header_coming = True
        for values in csv.UnicodeReader(self.stream):
            if not values:
                header_coming = True
            else:
                if header_coming:
                    # Model
                    model, first_field = values[0].split(':', 2)
                    try:
                        self.model = models.get_model(*model.split("."))
                    except TypeError:
                        raise base.DeserializationError("No model %s in db" % model)
                    # Field names
                    self.field_names = [first_field] + values[1:]
                    header_coming = False
                else:
                    # An object
                    meta = self.model._meta
                    data = {meta.pk.attname: meta.pk.to_python(values[0])}
                    m2m_data = {}
                    for i in range(1, len(values)):
                        name = self.field_names[i]
                        value = values[i]
                        field = meta.get_field(name)
                        if field.rel and isinstance(field.rel, models.ManyToManyRel):
                            m2m_data[field.name] = self.handle_m2m_field(value, field)
                        elif field.rel and isinstance(field.rel, models.ManyToOneRel):
                            data[field.attname] = self.handle_fk_field(value, field)
                        else:
                            data[field.name] = self.handle_field(value, field)
                    yield base.DeserializedObject(self.model(**data), m2m_data)

    def handle_field(self, raw, field):
        if raw == '':
            raw = None
        elif is_string_field(field):
            if spaces_re.match(raw):
                raw = raw[1:]
        return field.to_python(raw)

    def handle_fk_field(self, raw, field):
        if raw == '':
            return None
        related_field = field.rel.to._meta.get_field(field.rel.field_name)
        return related_field.to_python(raw)

    def handle_m2m_field(self, raw, field):
        if raw:
            return eval(raw)
        else:
            return []


def is_string_field(field):
    """If all field classes working with strings extended CharField, we
    wouldn't need this method"""

    from django.db.models.fields import CharField, FilePathField, SlugField, TextField
    from django.db.models.fields.files import FileField
    from django.contrib.localflavor.us.models import USStateField
 
    string_types = (CharField, FilePathField, SlugField, TextField,
                    FileField, USStateField)
    
    for s in string_types:
        if field.__class__ == s:
            return True

    return False    
