from contextlib import contextmanager
import logging
import sys

from fiftyfive.io import IOLogger

@contextmanager
def stdio_logger(sys_key, logger, level=logging.INFO):
    try:
        saved_io = sys.__dict__[sys_key]
        sys.__dict__[sys_key] = IOLogger(saved_io, logger, level)
        yield
    finally:
        sys.__dict__[sys_key] = saved_io

