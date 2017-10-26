# -*- coding: utf-8 -*-
"""
git helpers.
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from os import chmod

# 3rd party imports
from fabric.api import local

# local imports
from .common import _is_true, _repo_path, _sysmsg, _errmsg, _current_branch


def addgithooks():
    """ Setup project git hooks.

    This will run all the checks before pushing to avoid waiting for the CI
    fail.
    """
    _sysmsg("Adding pre-push hook")
    with open(_repo_path('.git/hooks/pre-push'), 'w') as fp:
        fp.write('\n'.join([
            '#!/bin/bash',
            'source ./env/bin/activate',
            'fab check',
            'fab fe_check'
        ]))

    _sysmsg("Making pre-push hook executable")
    chmod(_repo_path('.git/hooks/pre-push'), 0o755)


def push():
    """ Push the current branch and set to track remote. """
    branch = _current_branch()
    local('git push -u origin {}'.format(branch))


def merged(release='no'):
    """ Checkout develop, pull and delete merged branches.

    This is to ease the repetitive cleanup of each merged branch.
    """
    target_branch = 'release' if _is_true(release) else 'develop'
    branch = _current_branch()

    try:
        local('git rev-parse --verify {}'.format(branch))
    except:
        _errmsg("Branch '{}' does not exist".format(branch))

    _sysmsg("Checking out ^33{}".format(target_branch))
    local('git checkout {}'.format(target_branch))

    _sysmsg("Pulling latest changes")
    local('git pull origin {}'.format(target_branch))

    _sysmsg("Deleting branch ^33{}".format(branch))
    local('git branch -d {}'.format(branch))

    _sysmsg("Pruning")
    local('git fetch --prune origin')

    _sysmsg("Going back to ^33develop^32 branch")
    local('git checkout develop')
