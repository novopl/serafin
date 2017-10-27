# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
from unittest import TestCase
from datetime import datetime

# 3rd party imports
from jsobj import jsobj

# local imports
from ..core import dump_val
from ..serializers import serialize_primitive
from ..fieldspec import Fieldspec


class TestPrimitives(TestCase):
    def test_serialize_int(self):
        ctx = jsobj(dumpval=dump_val)
        out = serialize_primitive(5, Fieldspec('*'), ctx)
        self.assertEqual(out, 5)

    def test_serialize_None(self):
        ctx = jsobj(dumpval=dump_val)
        out = serialize_primitive(None, Fieldspec('*'), ctx)
        self.assertEqual(out, None)

    def test_serialize_str(self):
        ctx = jsobj(dumpval=dump_val)
        out = serialize_primitive('test str', Fieldspec('*'), ctx)
        self.assertEqual(out, 'test str')

    def test_serialize_datetime(self):
        dt = datetime(2015, 5, 1, 13, 21, 38)
        ctx = jsobj(dumpval=dump_val)
        out = serialize_primitive(dt, Fieldspec('*'), ctx)
        self.assertEqual(out, dt.isoformat())
