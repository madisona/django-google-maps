from unittest import TestCase
from ..fields import typename
from django.utils import six


class TypeNameTests(TestCase):

    def test_simple_type_returns_type_name_as_string(self):
        self.assertEqual("str", typename("x"))

    def test_class_object(self):
        class X:
            pass

        if six.PY2:
            expected_type = 'classobj'
        else:
            expected_type = 'type'

        self.assertEqual(expected_type, typename(X))
