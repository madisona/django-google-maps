from mock import patch, Mock

from django import test
from django.core import exceptions

from django_google_maps import fields

class GeoPtFieldTests(test.TestCase):

    def test_sets_lat_lon_on_initialization(self):
        geo_pt = fields.GeoPt("15.001,32.001")
        self.assertEqual(15.001, geo_pt.lat)
        self.assertEqual(32.001, geo_pt.lon)

    def test_uses_lat_comma_lon_as_unicode_representation(self):
        lat_lon_string = "15.001,32.001"
        geo_pt = fields.GeoPt(lat_lon_string)
        self.assertEqual(lat_lon_string, unicode(geo_pt))

    def test_two_GeoPts_with_same_lat_lon_should_be_equal(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = fields.GeoPt("15.001,32.001")
        self.assertEqual(geo_pt_1, geo_pt_2)

    def test_two_GeoPts_with_different_lat_should_not_be_equal(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = fields.GeoPt("20.001,32.001")
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_two_GeoPts_with_different_lon_should_not_be_equal(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = fields.GeoPt("15.001,62.001")
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_is_not_equal_when_comparison_is_not_GeoPt_object(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = "15.001,32.001"
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_allows_GeoPt_instantiated_with_empty_string(self):
        geo_pt = fields.GeoPt('')
        self.assertEqual(None, geo_pt.lat)
        self.assertEqual(None, geo_pt.lon)

    def test_uses_empty_string_as_unicode_representation_for_empty_GeoPt(self):
        geo_pt = fields.GeoPt('')
        self.assertEqual('', unicode(geo_pt))

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_splits_geo_point_on_comma(self):
        lat, lon = fields.GeoPt(Mock())._split_geo_point("15.001,32.001")
        self.assertEqual('15.001', lat)
        self.assertEqual('32.001', lon)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_error_when_attribute_error_on_split(self):
        geo_point = Mock()
        geo_point.split.side_effect = AttributeError

        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._split_geo_point, geo_point)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_error_when_type_error_on_split(self):
        geo_point = Mock()
        geo_point.split.side_effect = ValueError

        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._split_geo_point, geo_point)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_returns_float_value_when_valid_value(self):
        geo_pt = fields.GeoPt(Mock())
        val = geo_pt._validate_geo_range('45.005', 90)
        self.assertEqual(45.005, val)
        self.assertIsInstance(val, float)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_exception_when_type_error(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, object, 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_exception_when_value_error(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, 'a', 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_exception_when_value_is_out_of_upper_range(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, '90.01', 90)

    @patch("django_google_maps.fields.GeoPt.__init__", Mock(return_value=None))
    def test_raises_exception_when_value_is_out_of_lower_range(self):
        geo_pt = fields.GeoPt(Mock())
        self.assertRaises(exceptions.ValidationError, geo_pt._validate_geo_range, '-90.01', 90)
