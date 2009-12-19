import logging


class IOLogger(object):
    """
    A class that's meant to be substituted in for sys.stdout.
    It will output to both sys.stdout and the supplied logger.
    """

    def __init__(self, io_obj, logger, level=logging.INFO):
        self.logger = logger
        self.io = io_obj
        self.level = level

    def _log(self, s):
        if s.rstrip():
            self.logger.log(self.level, s.rstrip())

    def write(self, s):
        self.io.write(s)
        self._log(s)

    def readline(self, size=-1):
        s = self.io.readline(size)
        self._log(u"User input: %s" % s)
        return s

    def flush(self):
        pass
