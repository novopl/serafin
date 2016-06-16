#!/usr/bin/env python
import unittest

from igor.serialize.fieldspec import Fieldspec


class FieldspecTest(unittest.TestCase):
    def setUp(self):
        self.spec = Fieldspec('field1,field2(sub1,sub2),field3(*)')

    def test_creation(self):
        self.assertEqual(repr(self.spec), '<Fieldspec: field1,field2,field3>')

    def test_contains(self):
        self.assertIn('field1', self.spec)
        self.assertNotIn('field7', self.spec)

    def test_get_subspec(self):
        self.assertEqual(self.spec['field1'], True)

        self.assertEqual(repr(self.spec['field2']), '<Fieldspec: sub1,sub2>')
        self.assertEqual(self.spec['field2']['sub1'], True)
        self.assertIn('sub1', self.spec['field2'])

    def test_return_proper_for_star_fieldspec(self):
        spec = Fieldspec('*')
        self.assertTrue('test' in spec)
        self.assertTrue(spec['test'])

