from unittest import TestCase
from ..fields import typename


class TypeNameTests(TestCase):

    def test_simple_type_returns_type_name_as_string(self):
        self.assertEqual("str", typename("x"))

    def test_class_object(self):
        class X:
            pass
        self.assertEqual("classobj", typename(X))
