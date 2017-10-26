# -*- coding: utf-8 -*-
""" Frontend related commands.

All frontend commands should be implemented through
``src/frontend/package.json``. This is just a proxy to allow easily running
them from the root project directory.
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from fabric.api import local, lcd

# local imports
from . import config as conf
from .common import _errmsg


FRONTEND_PATH = conf.get('FRONTEND_PATH', None)


def fe_build():
    """ Build frontend. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm run build')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_dev():
    """ Live serve the frontend. For development. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm start')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_watch():
    """ Build frontend. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm run watch')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_test():
    """ Run frontend tests. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm test')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_lint():
    """ Lint frontend code. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm run lint')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_init():
    """ Lint frontend code. """
    if FRONTEND_PATH is not None:
        with lcd(FRONTEND_PATH):
            local('npm install')
    else:
        _errmsg("No FRONTEND_PATH defined in the config")


def fe_check():
    """ Run frontend lint and test as one command. """
    fe_lint()
    fe_test()
