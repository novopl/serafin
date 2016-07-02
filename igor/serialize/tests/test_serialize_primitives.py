# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from datetime import datetime
from igor.serialize.base import dumpval
from igor.serialize.fieldspec import Fieldspec
from igor.serialize.core_serializers import serialize_primitive, serialize_None


class TestPrimitives(TestCase):
    def test_serialize_int(self):
        out = serialize_primitive(5, Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertEqual(out, 5)

    def test_serialize_None(self):
        out = serialize_primitive(None, Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertEqual(out, None)

    def test_serialize_str(self):
        out = serialize_primitive('test str', Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertEqual(out, 'test str')

    def test_serialize_datetime(self):
        dt = datetime(2015, 5, 1, 13, 21, 38)
        out = serialize_primitive(dt, Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertEqual(out, dt.isoformat())
