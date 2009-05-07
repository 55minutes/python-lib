import os

from fiftyfive.utils import csv_ as csv

import python

class Serializer(python.Serializer):
    "Serialize a QuerySet to csv"

    def start_serialization(self):
        super(Serializer, self).start_serialization()
        # By default, csv module uses '\r\n' as lineterminator
        self.output = csv.UnicodeWriter(self.stream, lineterminator=os.linesep)

    def end_serialization(self):
        self.write_header()
        self.write_rows()

    def write_header(self):
        header = []
        header.append(self.get_string_value('%s:pk' %self.get_string_value(self.queryset.model._meta)))
        for f in self.fields:
            header.append(self.get_string_value(f))
        self.output.writerow(header)

    def write_rows(self):
        for obj in self.objects:
            row = []
            row.append(self.get_string_value(obj['pk']))
            for v in obj['fields'].itervalues():
                row.append(self.get_string_value(v))
            self.output.writerow(row)
