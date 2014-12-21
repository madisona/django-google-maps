import mock
from django import test
from django_google_maps import fields


class SouthTests(test.TestCase):

    def test_does_not_fail_when_south_is_not_installed(self):
        with mock.patch('south.modelsinspector.add_introspection_rules', side_effect=ImportError):
            with self.assertRaises(AssertionError):
                with self.assertRaises(ImportError):
                    reload(fields)
