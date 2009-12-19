from contextlib import nested
from functools import wraps
import logging

from contextmanagers import stdio_logger

def log_stdio(logger, level=logging.INFO):
    def decorate(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            with nested(stdio_logger('stdin', logger, level),
                        stdio_logger('stdout', logger, level),
                        stdio_logger('stderr', logger, level)):
                f(*args, **kwargs)
        return wrapper
    return decorate
