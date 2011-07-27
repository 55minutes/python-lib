import os

from fabric.api import *
from fabric.colors import green


def _dir_exists(p):
    if os.path.isdir(os.path.expanduser(p)):
        return p
    raise OSError("Not a valid path.")


def _check_for_scmdir():
    if not env._scmdir:
        prompt('Path to hg repository:', '_scmdir', validate=_dir_exists)
        env._scmdir = [env._scmdir]


def _cmd_loop(cmd):
    for d in env._scmdir:
        print green(d, bold=True)
        with lcd(os.path.expanduser(d)):
            local(cmd, capture=False)
        print


@runs_once
def scm_cmd(cmd):
    _check_for_scmdir()
    _cmd_loop(cmd)


# Subversion command
def svn(svn_cmds):
    """
    Specify svn_cmds as a string, such as svn:"log -l5".
    Perform `svn hg_cmds` for the given directories.
    """
    cmd = u'svn %(svn_cmds)s' % vars()
    scm_cmd(cmd)


# Mercurial commands
def hg(cmds):
    """
    Specify cmds as a string, such as hg:"log -l5".
    Perform `hg cmds` for the given directories.
    """
    cmd = u'hg %(cmds)s' % vars()
    with settings(warn_only=True):
        scm_cmd(cmd)
