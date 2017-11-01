# -*- coding: utf-8 -*-
"""
This is fabrics configuration file.
"""
from __future__ import absolute_import

# Configure the build
from ops.commands.common import conf
conf.init({
    'SRC_DIR': 'src',
    'SRC_PATH': 'src/serafin',
    'BUILD_DIR': '.build',
    'LINT_PATHS': [
        'src/serafin',
        'ops/commands',
        'test'
    ],
    'REFDOC_PATHS': [
        'src/serafin',
        'ops/commands',
    ],
    'TEST_TYPES': {
        'default': {'paths': [
            'test',
            'ops/commands',
        ]}
    }
})

# Import all commands
from ops.commands.clean import *
from ops.commands.docs import *
from ops.commands.git import *
from ops.commands.lint import *
from ops.commands.ops import *
from ops.commands.release import *
from ops.commands.test import *
