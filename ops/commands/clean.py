# -*- coding: utf-8 -*-
"""
Various commands that do not fit another category but there's not enough of them
to justify a separate module.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import os

# local imports
from . import config as conf
from .common import _rm_glob


CLEAN_PATTERNS = conf.get('CLEAN_PATTERNS', [
    '__pycache__',
    '*.py[cod]',
    '.swp',
])


def clean():
    """ Remove temporary files like python cache, swap files, etc. """
    cwd = os.getcwd()

    os.chdir(conf.repo_path('.'))

    for pattern in CLEAN_PATTERNS:
        _rm_glob(pattern)

    os.chdir(cwd)