# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from igor.serialize.base import dumpval
from igor.serialize.fieldspec import Fieldspec
from igor.serialize.core_serializers import serialize_iterable


class TestSerializeIterable(TestCase):
    def test_only_primitives_inside_one_level_deep(self):
        data = [1, 'test', 3.14159]
        out = serialize_iterable(data, Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertListEqual(out, data)

    def test_converts_string_to_Fieldspec(self):
        data = [1, 'test', 3.14159]
        out = serialize_iterable(data, '*', dumpval=dumpval, kwargs={})
        self.assertListEqual(out, data)
