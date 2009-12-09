from contextlib import contextmanager, nested
from functools import wraps
import logging
import sys


@contextmanager
def stdio_logger(sys_key, logger, level=logging.INFO):
    try:
        saved_io = sys.__dict__[sys_key]
        sys.__dict__[sys_key] = IOLogger(saved_io, logger, level)
        yield
    finally:
        sys.__dict__[sys_key] = saved_io


def log_stdio(logger, level=logging.INFO):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with nested(stdio_logger('stdin', logger),
                        stdio_logger('stdout', logger),
                        stdio_logger('stderr', logger)):
                f(*args, **kwargs)
        return wrapper
    return decorate


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
