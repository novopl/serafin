# -*- coding: utf-8 -*-
"""
Code linting commands.
"""
from __future__ import absolute_import, unicode_literals

# 3rd party imports
from six import string_types
from fabric.api import local

# local imports
from . import config as conf
from .common import _surround_paths_with_quotes
from .common import _sysmsg


PYLINT_CFG_PATH = conf.get(
    'PYLINT_CFG_PATH', conf.repo_path('ops/tools/pylint.ini')
)
PEP8_CFG_PATH = conf.get(
    'PEP8_CFG_PATH', conf.repo_path('ops/tools/pep8.ini')
)
PKGS_PATHS = conf.get('PKGS_PATHS', [])


def _lint_files(paths):
    """ Run static analysis on the given files.

    :param paths:   Iterable with each item being path that should be linted..
    """
    if isinstance(paths, string_types):
        raise ValueError("paths must be an array of strings")

    _sysmsg("Linting")
    for path in paths:
        print("--   {}".format(path))

    paths = _surround_paths_with_quotes(paths)

    _sysmsg("Checking PEP8 compatibility")
    pep8_cmd = 'pep8 --config {} {{}}'.format(PEP8_CFG_PATH)
    pep8_ret = local(pep8_cmd.format(paths)).return_code

    _sysmsg("Running linter")
    pylint_cmd = 'pylint --rcfile {} {{}}'.format(PYLINT_CFG_PATH)
    pylint_ret = local(pylint_cmd.format(paths)).return_code

    if pep8_ret != 0:
        print("pep8 failed with return code {}".format(pep8_ret))

    if pylint_ret:
        print("pylint failed with return code {}".format(pylint_ret))

    return pep8_ret == pylint_ret == 0


def lint():
    """ Run pep8 and pylint on all project files. """
    if not _lint_files(PKGS_PATHS):
        exit(1)