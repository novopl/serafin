# -*- coding: utf-8 -*-
# Copyright 2016-2019 Mateusz Klos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# pylint: disable=missing-docstring
from __future__ import absolute_import, unicode_literals

# stdlib imports
from unittest import TestCase

# local imports
from serafin import Context
from serafin.fieldspec import Fieldspec
from serafin.serializer import dump_val
from serafin.serializers import serialize_dict


class TestSerializeDict(TestCase):
    def test_only_primitives_inside_one_level_deep(self):
        data = {
            'field1':  123,
            'field2':  "string",
            'field3':  123.321,
            'field4':  {
                'field1': 3.14159,
                'field2': 'sub val'
            }
        }
        ctx = Context(dumpval=dump_val)
        result = serialize_dict(data, Fieldspec('*'), ctx)
        self.assertDictEqual(result, {
            'field1':  123,
            'field2':  "string",
            'field3':  123.321,
            'field4':  {}
        })

    def test_converts_string_to_fieldspec(self):
        ctx = Context(dumpval=dump_val)
        output = serialize_dict({'test': 123}, Fieldspec('*'), ctx)
        self.assertDictEqual(output, {'test': 123})
