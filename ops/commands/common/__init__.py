# -*- coding: utf-8 -*-
"""
Common code used by all commands.

All the functions are private so that fabric won't expose them as commands. This
can also be counter-acted by explicitly defining ``__all__`` but making them
private is less hassle. Just works and requires no manual management.
"""
from __future__ import absolute_import, unicode_literals

from .fs import _rm_glob
from .fs import _surround_paths_with_quotes
from .log import _cprint
from .log import _cstr
from .log import _errmsg
from .log import _sysmsg
from .project import _current_branch
from .project import _repo_path
from .project import _inside_repo
from .versioning import _bump_version
from .versioning import _bump_version_file
from .versioning import _get_current_version


def _is_true(value):
    """ Convert various string values to boolean. """
    return value.lower() in ('yes', 'y', 'true', 'on')
