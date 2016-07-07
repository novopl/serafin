#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import unittest
import json
from igor.serialize import serialize


class TestSerialize(unittest.TestCase):
    def _test_dict(self):
        return {
            'field1': 10,
            'field2': {
                'sub1': 1,
                'sub2': 2,
            },
            'field3': 20,
        }

    def test_serialize__all(self):
        model = self._test_dict()
        self.assertDictEqual(serialize(model, '*'), {
            'field1': 10,
            'field2': {},
            'field3': 20
        })

    def test_serialize__selected(self):
        model = self._test_dict()

        self.assertDictEqual(serialize(model, 'field1,field3'), {
            'field1': 10,
            'field3': 20
        })

    def test_serialize__expand_selected(self):
        model = self._test_dict()
        self.assertDictEqual(serialize(model, 'field1,field2(sub1)'), {
            'field1': 10,
            'field2': {
                'sub1': 1
            }
        })

    def test_serialize__expand_all(self):
        model = self._test_dict()
        self.assertDictEqual(serialize(model, 'field1,field2(*)'), {
            'field1': 10,
            'field2': {
                'sub1': 1,
                'sub2': 2
            }
        })

    def test_serialize__all_recursive(self):
        model = self._test_dict()

        self.assertDictEqual(serialize(model, '**'), {
            'field1': 10,
            'field2': {
                'sub1': 1,
                'sub2': 2
            },
            'field3': 20
        })