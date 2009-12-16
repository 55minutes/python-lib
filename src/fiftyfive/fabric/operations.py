from fabric.api import local as flocal

__all__ = ('local',)


def local(cmd, capture=False):
    return flocal(cmd, capture)
