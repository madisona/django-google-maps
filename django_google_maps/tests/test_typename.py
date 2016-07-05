from django import test
from django.utils import six
from django_google_maps.fields import typename


class TypeNameTests(test.TestCase):

    def test_simple_type_returns_type_name_as_string(self):
        self.assertEqual('str', typename("x"))

    def test_class_object(self):
        class X:
            pass

        if six.PY2:
            expected_type = 'classobj'
        else:
            expected_type = 'type'
        self.assertEqual(expected_type, typename(X))
