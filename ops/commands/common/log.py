# -*- coding: utf-8 -*-
"""
Helpers for nice shell output formatting.

.. autofunction:: _cstr
.. autofunction:: _sysmsg
.. autofunction:: _errmsg
"""
from __future__ import absolute_import, unicode_literals

# stdlib imports
import re


def _cstr(msg):
    """ Format color marked string into proper shell opcodes. """
    return re.sub(r'\^(\d{1,2})', '\x1b[\\1m', msg)


def _cprint(msg, *args, **kw):
    """ Print colored message to stdout. """
    if len(args) or len(kw):
        msg = msg.format(*args, **kw)

    print(_cstr(msg))


def _sysmsg(msg, *args, **kw):
    """ Print sys message to stdout.

    System messages should inform about the flow of the script. This should
    be a major milestones during the build.
    """
    if len(args) or len(kw):
        msg = msg.format(*args, **kw)

    print(_cstr('-- ^32{}^0'.format(msg)))


def _errmsg(msg, *args, **kw):
    """ Per step status messages

    Use this locally in a command definition to highlight more important
    information.
    """
    if len(args) or len(kw):
        msg = msg.format(*args, **kw)

    print(_cstr('^-- 31{}^0'.format(msg)))
