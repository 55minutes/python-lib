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


class UnicodeDictReader:
    """
    A CSV reader which will iterate over lines in the CSV file "f",
    which is encoded in the given encoding.
    """
    
    def __init__(self, f, fieldnames=None, restkey=None, restval=None,
                 dialect="excel", encoding="utf-8", *args, **kwds):
        self._fieldnames = fieldnames   # list of keys for the dict
        self.restkey = restkey          # key to catch long rows
        self.restval = restval          # default value for short rows
        self.reader = UnicodeReader(f, dialect, encoding, *args, **kwds)
        self.dialect = dialect
        self.line_num = 0

    def __iter__(self):
        return self

    def _get_fieldnames(self):
        if self._fieldnames is None:
            try:
                self._fieldnames = self.reader.next()
            except StopIteration:
                pass
        self.line_num = self.reader.line_num
        return self._fieldnames

    def _set_fieldnames(self, value):
        self._fieldnames = value
    fieldnames = property(_get_fieldnames, _set_fieldnames)

    def next(self):
        if self.line_num == 0:
            # Used only for its side effect.
            self.fieldnames
        row = self.reader.next()
        self.line_num = self.reader.line_num

        # unlike the basic reader, we prefer not to return blanks,
        # because we will typically wind up with a dict full of None
        # values
        while row == []:
            row = self.reader.next()
        d = dict(zip(self.fieldnames, row))
        lf = len(self.fieldnames)
        lr = len(row)
        if lf < lr:
            d[self.restkey] = row[lf:]
        elif lf > lr:
            for key in self.fieldnames[lr:]:
                d[key] = self.restval
        return d


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
