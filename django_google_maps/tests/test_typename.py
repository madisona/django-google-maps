from __future__ import unicode_literals

from unittest import TestCase
from ..fields import typename
from django.utils import six


class TypeNameTests(TestCase):

    def test_simple_type_returns_type_name_as_string(self):
        self.assertEqual(six.text_type.__name__, typename("x"))

    def test_class_object(self):
        class X:
            pass

        if six.PY2:
            expected_type = 'classobj'
        else:
            expected_type = 'type'

        self.assertEqual(expected_type, typename(X))
