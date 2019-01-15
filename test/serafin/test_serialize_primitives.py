# -*- coding: utf-8 -*-
# Copyright 2017-2019 Mateusz Klos
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
from datetime import datetime

# local imports
from serafin import Context
from serafin.fieldspec import Fieldspec
from serafin.serializer import dump_val
from serafin.serializers import serialize_primitive


class TestPrimitives(TestCase):
    def test_serialize_int(self):
        ctx = Context(dumpval=dump_val)
        out = serialize_primitive(5, Fieldspec('*'), ctx)
        self.assertEqual(out, 5)

    def test_serialize_None(self):
        ctx = Context(dumpval=dump_val)
        out = serialize_primitive(None, Fieldspec('*'), ctx)
        self.assertEqual(out, None)

    def test_serialize_str(self):
        ctx = Context(dumpval=dump_val)
        out = serialize_primitive('test str', Fieldspec('*'), ctx)
        self.assertEqual(out, 'test str')

    def test_serialize_datetime(self):
        dt = datetime(2015, 5, 1, 13, 21, 38)
        ctx = Context(dumpval=dump_val)
        out = serialize_primitive(dt, Fieldspec('*'), ctx)
        self.assertEqual(out, dt.isoformat())
