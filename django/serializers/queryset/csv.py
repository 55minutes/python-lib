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
        r1 = self.objects[0]
        header.append(self.get_string_value('%s:pk' %r1['model']))
        for k in r1['fields']:
            header.append(self.get_string_value(k))
        self.output.writerow(header)

    def write_rows(self):
        for obj in self.objects:
            row = []
            row.append(self.get_string_value(obj['pk']))
            for v in obj['fields'].itervalues():
                row.append(self.get_string_value(v))
            self.output.writerow(row)
