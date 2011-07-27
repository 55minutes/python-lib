from contextlib import nested
import glob
import os
import re
from tempfile import mkdtemp
from urlparse import urljoin

from fabric.api import *
from fabric.contrib.files import upload_template
from fiftyfive.fabric.api import *

__all__ = []


def command(func):
    global __all__
    __all__.append(func.__name__)
    return func


def _ve_run(cmd):
    ve = env._virtualenv
    with prefix('workon %(ve)s' % vars()):
        r = run('%(cmd)s' % vars())
    return r


def make_distributions():
    env._tempdir = mkdtemp()
    tempdir = env._tempdir

    for s, sdict in env._sources.iteritems():
        with lcd(tempdir):
            local('svn co %s %s' % (sdict['svn_url'], s))

        sdict['wcdir'] = os.path.join(tempdir, s)
        sdict['distdir'] = os.path.join(sdict['wcdir'], 'dist')

        with lcd(sdict['wcdir']):
            if env._is_production:
                local('./setup.py egg_info -RDb "" sdist')
            else:
                local('./setup.py sdist')
            os.chdir(sdict['distdir'])
            sdict['sdist'] = glob.glob('*')[0]
            sdict['sdist_path'] = os.path.join(sdict['distdir'], sdict['sdist'])


def upload_distributions():
    staging_dir = env._remote_tempdir
    host = env.host
    port = env.port
    user = env.user

    for sdict in env._sources.itervalues():
        sdist = sdict['sdist_path']
        local('scp -P %(port)s %(sdist)s %(user)s@%(host)s:%(staging_dir)s' %
               vars())


def mkvirtualenv():
    run('mkvirtualenv %s --no-site-packages' % env._virtualenv)


def make_remote_tempdir():
    env._remote_tempdir = run("python -c 'from tempfile import mkdtemp;print mkdtemp()'")
    env._remote_tempdir = env._remote_tempdir.strip()


def upload_deploy_dependencies():
    template = os.path.join(env._sources['project']['wcdir'],
                            'dependencies', 'deploy.txt')
    f = open(template, 'a+')
    for sdict in env._sources.itervalues():
        print >> f, sdict['sdist']
    f.close()
    put(template, env._remote_tempdir)


def upload_uninstall_dependencies():
    template = os.path.join(env._sources['project']['wcdir'],
                            'dependencies', 'uninstall.txt')
    f = open(template, 'w')
    for sdict in env._sources.itervalues():
        distro = sdict['sdist'].split('.')[0]
        distro = re.match('(.*)-(.*)', distro).group(1)
        print >> f, distro
    f.close()
    put(template, env._remote_tempdir)


def uninstall_distributions():
    with nested(cd(env._remote_tempdir), settings(warn_only=True)):
        _ve_run('pip uninstall -y -r uninstall.txt')


def install_distributions():
    with cd(env._remote_tempdir):
        pip_cache = run('python -c \'import os;print os.path.expanduser("~/.pip")\'')
        pip_cache = pip_cache.strip()
        _ve_run('pip install -r deploy.txt --download-cache=%(pip_cache)s' % vars())


def upload_setting_overrides():
    fname = os.path.join(env._tempdir, 'settings.py')
    f = open(fname, 'w')
    f.write(env._setting_overrides)
    f.close()
    put(fname, os.path.join(env._sitepackages,
                            *env._django_settings_module.split('.')[:-1]))


def upload_wsgi_handler():
    template = os.path.join(env._sources['project']['wcdir'], 'src', 'scripts',
                            'handlers', 'django.wsgi')
    context = dict(django_settings = env._django_settings_module)
    upload_template(template, os.path.join(env._sitepackages, 'scripts',
                                           'handlers'), context)


def tag_installation():
    with cd(env._remote_tempdir):
        _ve_run('pip freeze > freeze.txt')
    get(os.path.join(env._remote_tempdir, 'freeze.txt'),
        os.path.join(env._sources['project']['wcdir'], 'dependencies'))
    with lcd(env._sources['project']['wcdir']):
        tag_name = os.path.splitext(
            os.path.splitext(env._sources['project']['sdist'])[0])[0]
        tag_url = urljoin(env._svn_tag_path, tag_name)
        local('svn copy . %(tag_url)s -m "Adding deployment tag."' % vars())
        local('svn switch %(tag_url)s' % vars())
        local('svn add dependencies/freeze.txt')
        local('svn ci -m "Adding frozen dependencies."')


@command
def pg_dump():
    dbname = env._dbname
    outfile = env._db_backup_file
    run('pg_dump %(dbname)s | gzip > %(outfile)s.gz' % vars())


@command
def deploy():
    if env._is_production:
        pg_dump()
    make_distributions()
    make_remote_tempdir()
    upload_distributions()
    mkvirtualenv()
    upload_deploy_dependencies()
    upload_uninstall_dependencies()
    uninstall_distributions()
    install_distributions()
    upload_setting_overrides()
    upload_wsgi_handler()
    if env._tag_svn:
        tag_installation()


@command
def rmvirtualenv():
    run('rmvirtualenv %s' % env._virtualenv)
