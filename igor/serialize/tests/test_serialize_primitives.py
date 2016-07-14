# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from igor.serialize.base import dumpval
from igor.serialize.fieldspec import Fieldspec
from igor.serialize.core_serializers import serialize_primitive
from igor.js import jsobj


class TestPrimitives(TestCase):
    def test_serialize_int(self):
        ctx = jsobj(dumpval=dumpval)
        out = serialize_primitive(5, Fieldspec('*'), ctx)
        self.assertEqual(out, 5)

    def test_serialize_None(self):
        ctx = jsobj(dumpval=dumpval)
        out = serialize_primitive(None, Fieldspec('*'), ctx)
        self.assertEqual(out, None)

    def test_serialize_str(self):
        ctx = jsobj(dumpval=dumpval)
        out = serialize_primitive('test str', Fieldspec('*'), ctx)
        self.assertEqual(out, 'test str')

    def test_serialize_datetime(self):
        dt = datetime(2015, 5, 1, 13, 21, 38)
        ctx = jsobj(dumpval=dumpval)
        out = serialize_primitive(dt, Fieldspec('*'), ctx)
        self.assertEqual(out, dt.isoformat())
