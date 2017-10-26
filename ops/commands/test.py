# -*- coding: utf-8 -*-
"""
Testing commands
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
from os.path import join

# 3rd party imports
from fabric.api import local, shell_env

# local imports
from . import config as conf
from .common import _is_true, _surround_paths_with_quotes


BUILD_DIR = conf.get('BUILD_DIR', conf.repo_path('.build'))

DEFAULT_PYTEST_CFG = conf.repo_path('ops/tools/pytest.ini')
PYTEST_CFG_PATH = conf.get('PYTEST_CFG_PATH', DEFAULT_PYTEST_CFG)
TEST_TYPES = conf.get('TEST_TYPES', {})

DEFAULT_COVERAGE_CFG = conf.repo_path('ops/tools/coverage.ini')
COVERAGE_OUT_PATH = join(BUILD_DIR, 'coverage')
COVERAGE_CFG_PATH = conf.get('COVERAGE_CFG_PATH', DEFAULT_PYTEST_CFG)

DJANGO_SETTINGS = conf.get('DJANGO_SETTINGS', None)
DJANGO_TEST_SETTINGS = conf.get('DJANGO_TEST_SETTINGS', None)


def test(**opts):
    """ Run all tests against the current python version. """
    args = []
    sugar = _is_true(opts.get('sugar', 'on'))
    junit = _is_true(opts.get('junit', 'off'))
    test_type = opts.get('type', 'default')
    verbose = int(opts.get('verbose', '0'))
    show_locals = _is_true(opts.get('locals', 'on'))
    coverage = _is_true(opts.get('coverage', 'on'))

    if coverage:
        args += [
            '--durations=3',
            '--cov-config={}'.format(COVERAGE_CFG_PATH),
            '--cov={}'.format(conf.SRC_PATH),
            '--cov-report=term:skip-covered',
            '--cov-report=html:{}'.format(COVERAGE_OUT_PATH),
        ]

    if junit:
        args += ['--junitxml={}/test-results.xml'.format('.build')]

    if DJANGO_TEST_SETTINGS is not None:
        args += ['--ds {}'.format(DJANGO_TEST_SETTINGS)]
    elif DJANGO_SETTINGS is not None:
        args += ['--ds {}'.format(DJANGO_SETTINGS)]

    if not sugar:
        args += ['-p no:sugar']

    if verbose >= 1:
        args += ['-v']
    if verbose >= 2:
        args += ['--full-trace']

    if show_locals:
        args += ['-l']

    test_config = {'paths': conf.SRC_PATH}
    if test_type is not None:
        test_config = TEST_TYPES.get(test_type)
        args += ['-m "{}"'.format(test_config['mark'])]

    with shell_env(PYTHONPATH=conf.SRC_DIR):
        test_paths = test_config['paths'] or []
        local('pytest -c {conf} {args} {paths}'.format(
            conf=PYTEST_CFG_PATH,
            args=' '.join(args),
            paths=_surround_paths_with_quotes(test_paths)
        ))
