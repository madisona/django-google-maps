from __future__ import unicode_literals

from django.core import exceptions
from django.test import TestCase
from django.utils import six

from ..fields import GeoPt


class GeoPtFieldTests(TestCase):

    def test_sets_lat_lon_on_initialization(self):
        geo_pt = GeoPt("15.001,32.001")
        self.assertEqual(15.001, geo_pt.lat)
        self.assertEqual(32.001, geo_pt.lon)

    def test_uses_lat_comma_lon_as_unicode_representation(self):
        lat_lon_string = "15.001,32.001"
        geo_pt = GeoPt(lat_lon_string)
        self.assertEqual(lat_lon_string, six.text_type(geo_pt))

    def test_two_GeoPts_with_same_lat_lon_should_be_equal(self):
        geo_pt_1 = GeoPt("15.001,32.001")
        geo_pt_2 = GeoPt("15.001,32.001")
        self.assertEqual(geo_pt_1, geo_pt_2)

    def test_two_GeoPts_with_different_lat_should_not_be_equal(self):
        geo_pt_1 = GeoPt("15.001,32.001")
        geo_pt_2 = GeoPt("20.001,32.001")
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_two_GeoPts_with_different_lon_should_not_be_equal(self):
        geo_pt_1 = GeoPt("15.001,32.001")
        geo_pt_2 = GeoPt("15.001,62.001")
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_is_not_equal_when_comparison_is_not_GeoPt_object(self):
        geo_pt_1 = GeoPt("15.001,32.001")
        geo_pt_2 = "15.001,32.001"
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_allows_GeoPt_instantiated_with_empty_string(self):
        geo_pt = GeoPt('')
        self.assertEqual(None, geo_pt.lat)
        self.assertEqual(None, geo_pt.lon)

    def test_uses_empty_string_as_unicode_representation_for_empty_GeoPt(self):
        geo_pt = GeoPt('')
        self.assertEqual('', six.text_type(geo_pt))

    def test_splits_geo_point_on_comma(self):
        pt = GeoPt("15.001,32.001")
        self.assertEqual('15.001', six.text_type(pt.lat))
        self.assertEqual('32.001', six.text_type(pt.lon))

    def test_raises_error_when_attribute_error_on_split(self):
        class Fake(object):
            pass
        with self.assertRaises(exceptions.ValidationError):
            GeoPt(Fake)

    def test_raises_error_when_type_error_on_split(self):
        with self.assertRaises(exceptions.ValidationError):
            x, y = GeoPt("x,x")

    def test_returns_float_value_when_valid_value(self):
        geo_pt = GeoPt('45.005,180')
        self.assertEqual(45.005, geo_pt.lat)

    def test_raises_exception_when_value_is_out_of_upper_range(self):
        with self.assertRaises(exceptions.ValidationError):
            GeoPt('180,180')

    def test_raises_exception_when_value_is_out_of_lower_range(self):
        with self.assertRaises(exceptions.ValidationError):
            GeoPt('-180,180')

    def test_len_returns_len_of_unicode_value(self):
        geo_pt = GeoPt("84,12")
        self.assertEqual(9, len(geo_pt))
