# -*- coding: utf-8 -*-
"""
Project configuration file
"""
from __future__ import absolute_import, unicode_literals
from os.path import dirname, join, normpath


def repo_path(path):
    """ Return absolute path to the repo dir (root project directory). """
    return normpath(join(dirname(__file__), '../..', path))


# general
SRC_DIR = repo_path('src')
SRC_PATH = repo_path('src/simplechat')
BUILD_DIR = repo_path('.build')
PKGS_PATHS = [
    repo_path('ops/commands'),
]
TEST_TYPES = {
    'default': {'paths': PKGS_PATHS}
}


def get(name, *default):
    """ get config value with the given name and optional default.

    :param str|unicode name:
        The name of the config value.
    :param Any default:
        If given and the key doesn't not exist, this will be returned instead.
        If it's not given and the config value does not exist, AttributeError
        will be raised
    :return Any:
        The requested config value. This is one of the global values defined
        in this file.

    """
    g = globals()
    if name in g:
        return g[name]
    elif default:
        return default[0]
    else:
        raise AttributeError("Config value '{}' does not exist".format(name))
