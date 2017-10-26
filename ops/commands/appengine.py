# -*- coding: utf-8 -*-
"""
Commands related to Google AppEngine.

Only useful on appengine projects. If you're not using AppEngine, do not
import those into your fabfile.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import sys
import os
from os.path import join, exists

# local imports
from .common import _cprint


def _is_appengine_sdk(path):
    """ Return True if the given *path* contains AppEngine SDK. """
    return all(exists(join(path, f)) for f in (
        'appcfg.py',
        'dev_appserver.py',
        'google',
        'lib',
    ))


def _find_appengine_sdk():
    """ Find appengine_sdk in the current $PATH. """
    paths = sys.path + os.environ.get('PATH').split(':')
    sdk_path = next((path for path in paths if _is_appengine_sdk(path)), None)

    if sdk_path is None:
        msg_lines = (
            '^91AppEngine SDK not found!^0',
            '^90m',
            '   The Google AppEngine SDK must be in your ^1$PATH^90 or you can'
            ' use  ^1$APPENGINE_SDK^90 environment variable to specify it'
            ' directly.',
            '^0'
        )
        _cprint('\n'.join(msg_lines))
        sys.exit(1)

    return sdk_path
