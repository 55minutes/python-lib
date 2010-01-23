from fabric.api import *
from fiftyfive.fabric.api import *

from management import _local_or_run

__all__ = []


def command(func):
    global __all__
    __all__.append(func.__name__)
    return func


@command
def loaddata():
    fixtures = ' '.join(env._fixtures)
    _local_or_run('manage loaddata %(fixtures)s' % vars())


@command
def syncdb():
    _local_or_run('manage syncdb --noinput')


@command
def initdata():
    if env.host:
        run('createdb -w %s' % env._dbname)
    syncdb()
    loaddata()


@command
def dropdb():
    if env.host:
        run('dropdb -w %s' % env._dbname)
    else:
        local('rm %s' %env._settings.DATABASE_NAME)


@command
def resetdb():
    with settings(warn_only=True):
        dropdb()
    initdata()
