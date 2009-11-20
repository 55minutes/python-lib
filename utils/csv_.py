import csv
import codecs
import StringIO


class UTF8Recoder:
    """
    Iterator that reads an encoded stream and reencodes the input to UTF-8
    """

    def __init__(self, f, encoding):
        self.reader = codecs.getreader(encoding)(f)

    def __iter__(self):
        return self

    def next(self):
        return self.reader.next().encode("utf-8")


class ReaderInterface:
    """
    CSV reader interfaces.
    """

    def _dialect(self):
        return self.reader.dialect
    dialect = property(_dialect)

    def _line_num(self):
        return self.reader.line_num
    line_num = property(_line_num)

    def _fieldnames(self):
        return self.reader.fieldnames
    fieldnames = property(_fieldnames)


class UnicodeReader(ReaderInterface):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.reader(f, dialect=dialect, **kwds)

    def next(self):
        row = self.reader.next()
        return [unicode(s, "utf-8") for s in row]

    def __iter__(self):
        return self


class UnicodeDictReader(ReaderInterface):
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect=csv.excel, encoding="utf-8", *args, **kwds):
        f = UTF8Recoder(f, encoding)
        self.reader = csv.DictReader(
            f, fieldnames=fieldnames, restkey=restkey, restval=restval,
            dialect=dialect, *args, **kwds)

    def next(self):
        row_dict = {}
        for k, v in self.reader.next().iteritems():
            row_dict[unicode(k, 'utf-8')] = unicode(v, 'utf-8')
        return row_dict

    def __iter__(self):
        return self


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getencoder(encoding)

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data, length = self.encoder(data)
        # write to the target stream
        self.stream.write(data)
        # reinitialize the queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
