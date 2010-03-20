from fabric.api import *
from fiftyfive.fabric.api import *

from management import _local_or_run
from management_extras import *

__all__ = []


def command(func):
    global __all__
    __all__.append(func.__name__)
    return func


@command
def resetdb():
    with settings(warn_only=True):
        dropdb()
    initdata()


@command
def initdata():
    if env.host:
        run('createdb -w %s' % env._dbname)
    syncdb()
    migrate()
    loaddata()


@command
def south_init():
    _local_or_run('manage syncdb && manage migrate 0001 --all --fake')


@command
def migrate():
    _local_or_run('manage migrate --all --no-initial-data')
