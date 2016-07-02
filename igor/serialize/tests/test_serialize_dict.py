# -*- coding: utf-8 -*-
from __future__ import absolute_import
from unittest import TestCase
from igor.serialize.base import dumpval
from igor.serialize.fieldspec import Fieldspec
from igor.serialize.core_serializers import serialize_dict


class TestSerializeDict(TestCase):
    def test_only_primitives_inside_one_level_deep(self):
        input = {
            'field1':  123,
            'field2':  "string",
            'field3':  123.321,
            'field4':  {
                'field1': 3.14159,
                'field2': 'sub val'
            }
        }
        output = serialize_dict(input, Fieldspec('*'), dumpval=dumpval, kwargs={})
        self.assertDictEqual(output, {
            'field1':  123,
            'field2':  "string",
            'field3':  123.321,
            'field4':  {}
        })

    def test_converts_string_to_Fieldspec(self):
        output = serialize_dict({'test': 123}, '*', dumpval=dumpval, kwargs={})
        self.assertDictEqual(output, {'test': 123})

