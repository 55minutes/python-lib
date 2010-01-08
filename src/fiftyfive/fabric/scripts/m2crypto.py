import os
from tempfile import mkstemp

from fabric.api import *
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


FEDORA_SETUP = """\
#!/bin/sh

arch=`uname -i`
for i in SWIG/_{ec,evp}.i; do
  sed -i -e "s/opensslconf.*\./opensslconf-${arch}\./" "$i"
done

SWIG_FEATURES=-cpperraswarn python setup.py $*
"""
@command
def m2crypto():
    mkvirtualenv()
    make_remote_tempdir()
    fd, fpath = mkstemp()
    of = os.fdopen(fd, 'w')
    of.write(FEDORA_SETUP)
    of.close()
    with cd(env._remote_tempdir):
        _ve_run('pip install -d . m2crypto')
        tgz_file = run('ls')
        run('tar -zxf %(tgz_file)s' % vars())
    m2crypto_dir = os.path.splitext(os.path.splitext(tgz_file)[0])[0]
    put(fpath, os.path.join(env._remote_tempdir, m2crypto_dir,
                            'fedora_setup.sh'))
    with cd(os.path.join(env._remote_tempdir, m2crypto_dir)):
        run('chmod +x fedora_setup.sh')
        _ve_run('./fedora_setup.sh install')
