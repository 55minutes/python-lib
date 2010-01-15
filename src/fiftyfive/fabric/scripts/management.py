from functools import wraps
import inspect
import os

from fabric.api import *
from fiftyfive.fabric.api import *
from fiftyfive.fabric.scripts.deploy import _ve_run

__all__ = []


env._apps_data = 'sample_data.json'
env._fixtures = [env._apps_data]


def command(func):
    global __all__
    __all__.append(func.__name__)
    return func


def set_django_environment(settings_module):
    os.environ['DJANGO_SETTINGS_MODULE'] = settings_module
    from django.conf import settings as django_settings
    env._settings = django_settings
    env._fixture_dir = django_settings.FIXTURE_DIRS[0]
    env._apps_fixture = os.path.join(env._fixture_dir, env._apps_data)
    env._database_engine = django_settings.DATABASE_ENGINE


def _local_or_run(cmd, capture=False):
    if env.host:
        caller = inspect.stack()[1][3]
        _ve_run('projectfab %(caller)s' % vars())
    else:
        local(cmd, capture)


@command
def graph_models():
    apps = env._apps
    outfile = env._model_graph_file
    local('manage graph_models %(apps)s -g -o %(outfile)s' % vars()) 


@command
def echo_fixturedir():
    print env._fixture_dir


@command
def dump_apps_data():
    apps = env._apps
    fixture = env._apps_fixture
    _local_or_run('manage dumpdata --indent=2 %(apps)s > %(fixture)s' % vars())


def create_update_with_remote_fixtures(dumpdata_func):
    def decorator(func):
        @wraps(func)
        def update_func():
            if len(env.hosts) != 1:
                abort("Requires one and *only* one remote host.")
            if not env._is_production:
                cont = prompt(
                    'Update fixtures from non-production environment? (Y/n)',
                    default='n', validate=r'[Y|n]')
                cont = (cont=='Y' and True) or (cont=='n' and False)
            else:
                cont = True
            if not cont:
                abort('Updating of fixtures aborted.')
            dumpdata_func()
            remote_dir = _ve_run(
                'projectfab echo_fixturedir').split(os.linesep)[0].strip()
            for f in env._fixtures:
                remote_sample = os.path.join(remote_dir, f)
                run('bzip2 -f %(remote_sample)s' % vars())
                get('%(remote_sample)s.bz2' % vars(), env._fixture_dir)
                run('bunzip2 -f %(remote_sample)s.bz2' % vars())
                local_sample = os.path.join(env._fixture_dir, f)
                local('bunzip2 -f %(local_sample)s.bz2' % vars())
        return update_func
    return decorator


@command
def manage(cmd):
    _ve_run('manage %(cmd)s' % vars())
