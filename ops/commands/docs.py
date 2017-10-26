# -*- coding: utf-8 -*-
"""
Various commands that do not fit another category but there's not enough of them
to justify a separate module.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import os
from os.path import exists, join
from shutil import rmtree

# 3rd party imports
from fabric.api import local, lcd
from refdoc import generate_docs as _generate_docs

# local imports
from . import config as conf
from .common import _sysmsg, _is_true, _errmsg


BUILD_DIR = conf.get('BUILD_DIR', '.build')
DOC_SRC_PATH = conf.get('DOC_SRC_PATHS', conf.repo_path('docs'))
PKGS_PATHS = conf.get('PKGS_PATHS', [])

DOC_OUT_PATH = join(DOC_SRC_PATH, 'html')
DOC_REF_PATH = join(DOC_SRC_PATH, 'ref')
DOC_ASSETS_PATH = join(DOC_SRC_PATH, 'assets')
DOC_BUILD_PATH = join(BUILD_DIR, 'docs')


def docs(recreate='no'):
    """ Build project documentation. """
    _sysmsg('Ensuring assets directory ^94{}^32 exists', DOC_ASSETS_PATH)
    if not exists(DOC_ASSETS_PATH):
        os.makedirs(DOC_ASSETS_PATH)

    if _is_true(recreate) and exists(DOC_OUT_PATH):
        _sysmsg("^91Deleting ^94{}".format(DOC_OUT_PATH))
        rmtree(DOC_OUT_PATH)

    if DOC_REF_PATH:
        _sysmsg('Removing previously generated reference documentation')
        if exists(DOC_REF_PATH):
            rmtree(DOC_REF_PATH)

        os.makedirs(DOC_REF_PATH)

        _sysmsg('Generating reference documentation')
        _generate_docs(PKGS_PATHS, out_dir=DOC_REF_PATH)
    else:
        _errmsg('Not generating any reference documentation - '
                'No DOC_REF_PKG_PATHS specified in config')

    with lcd(DOC_SRC_PATH):
        _sysmsg('Building docs with ^35sphinx')
        local('sphinx-build -b html -d {build} {docs} {out}'.format(
            build=DOC_BUILD_PATH,
            docs=DOC_SRC_PATH,
            out=DOC_OUT_PATH,
        ))
