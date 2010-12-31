
from mock import patch, Mock

from django import test
from django.core import exceptions

from django_google_maps import fields

class GeoPtFieldTests(test.TestCase):

    def should_set_lat_lon_on_initialization(self):
        geo_pt = fields.GeoPt("15.001,32.001")
        self.assertEqual(15.001, geo_pt.lat)
        self.assertEqual(32.001, geo_pt.lon)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_split_geo_point_on_comma(self):
        lat, lon = fields.GeoPt(Mock())._split_geo_point("15.001,32.001")
        self.assertEqual('15.001', lat)
        self.assertEqual('32.001', lon)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_error_when_attribute_error_on_split(self):
        geo_point = Mock()
        geo_point.split.side_effect = AttributeError

        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._split_geo_point, geo_point)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_error_when_type_error_on_split(self):
        geo_point = Mock()
        geo_point.split.side_effect = ValueError

        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._split_geo_point, geo_point)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_return_float_value_when_valid_value(self):
        geo_pt = fields.GeoPt(Mock())
        val = geo_pt._validate_geo_range('45.005', 90)
        self.assertEqual(45.005, val)
        self.assertIsInstance(val, float)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_exception_when_type_error(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, object, 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_exception_when_value_error(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, 'a', 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_exception_when_value_is_out_of_upper_range(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, '90.01', 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def should_raise_exception_when_value_is_out_of_lower_range(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, '-90.01', 90)