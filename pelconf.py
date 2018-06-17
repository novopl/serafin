# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from peltak.core import conf
conf.init({
    'SRC_DIR': 'src',
    'SRC_PATH': 'src/serafin',
    'BUILD_DIR': '.build',
    'LINT_PATHS': [
        'src/serafin',
        'test'
    ],
    'REFDOC_PATHS': [
        'src/serafin',
    ],
    'TEST_TYPES': {
        'default': {'paths': [
            'test',
        ]}
    }
})

# Import all commands
from peltak.commands import clean
from peltak.commands import docs
from peltak.commands import git
from peltak.commands import lint
from peltak.commands import release
from peltak.commands import test
from peltak.commands import version
