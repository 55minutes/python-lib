class StdIOLogger(object):
    """
    A class that's meant to be substituted in for sys.stdout.
    It will output to both sys.stdout and the supplied logger.
    """

    def __init__(self, stdio, logger, level=logging.INFO):
        self.logger = logger
        self.stdio = stdio
        self.level = level

    def _log(self, s):
        if s.rstrip():
            self.logger.log(self.level, s.rstrip())

    def write(self, s):
        self.stdio.write(s)
        self._log(s)

    def readline(self, size=-1):
        s = self.stdio.readline(size)
        self._log(u"User input: %s" % s)
        return s

    def flush(self):
        pass
