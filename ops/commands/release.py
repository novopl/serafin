# -*- coding: utf-8 -*-
"""
Helper commands for releasing to pypi.
"""
from __future__ import absolute_import, unicode_literals
from fabric.api import local

from . import config as conf
from .common import _bump_version_file
from .common import _get_current_version
from .common import _inside_repo
from .common import _sysmsg


VERSION_FILE = conf.get('VERSION_FILE', conf.repo_path('VERSION'))


def version():
    """ Return current project version. """
    ver = _get_current_version(VERSION_FILE)

    _sysmsg("Version: ^35{}".format(ver))


def bump_version(component='patch'):
    """ Bump current project version without committing anything.

    No tags are created either.
    """
    _sysmsg("Bumping package version")
    old_ver, new_ver = _bump_version_file(VERSION_FILE, component)

    _sysmsg("  old version: ^35{}".format(old_ver))
    _sysmsg("  new version: ^35{}".format(new_ver))


def make_release(component='patch'):
    """ Release a new version of the project.

    This will bump the version number (patch component by default) + add and tag
    a commit with that change. Finally it will upload the package to pypi.
    """
    with _inside_repo(quiet=True):
        git_status = local('git status --porcelain', capture=True).strip()
        has_changes = len(git_status) > 0

    if has_changes:
        _sysmsg("Cannot release: there are uncommitted changes")
        exit(1)

    _sysmsg("Bumping package version")
    old_ver, new_ver = _bump_version_file(VERSION_FILE, component)

    _sysmsg("  old version: ^35{}".format(old_ver))
    _sysmsg("  new version: ^35{}".format(new_ver))

    with _inside_repo(quiet=True):
        _sysmsg("Creating commit for the release")
        local('git add {ver_file} && git commit -m "Release: v{ver}"'.format(
            ver_file=VERSION_FILE,
            ver=new_ver
        ))

        _sysmsg("Creating tag that marks the release")
        local('git tag -a "v{0}" -m "Mark v{0} release"'.format(new_ver))


def upload(target='local'):
    """ Release to a given pypi server ('local' by default). """
    _sysmsg("Uploading to pypi server ^33{}".format(target))
    with _inside_repo(quiet=False):
        local('python setup.py sdist register -r "{}"'.format(target))
        local('python setup.py sdist upload -r "{}"'.format(target))


def release(component='patch', target='local'):
    """ Release a new version of the project.

    This will bump the version number (patch component by default) + add and tag
    a commit with that change. Finally it will upload the package to pypi.
    """
    make_release(component)
    upload(target)
