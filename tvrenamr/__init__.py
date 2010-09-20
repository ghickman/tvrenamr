from tvrenamr import run

__author__ = 'George Hickman'
__versioninfo__ = (2, 2, 0)
__version__ = '.'.join(map(str, __versioninfo__))

def get_version():
    # need to work out how to use this to give the version to optparse
    return __version__


__all__ = ['run']