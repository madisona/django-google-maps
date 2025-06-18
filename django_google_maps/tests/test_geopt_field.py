from django import test
from django.core import exceptions
from django.utils.encoding import force_str

from django_google_maps import fields


class GeoPtFieldTests(test.TestCase):
    def test_sets_lat_lon_on_initialization(self):
        geo_pt = fields.GeoPt("15.001,32.001")
        self.assertEqual(15.001, geo_pt.lat)
        self.assertEqual(32.001, geo_pt.lon)

    def test_uses_lat_comma_lon_as_unicode_representation(self):
        lat_lon_string = "15.001,32.001"
        geo_pt = fields.GeoPt(lat_lon_string)
        self.assertEqual(lat_lon_string, force_str(geo_pt))

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

    def test_is_equal_when_comparison_str_GeoPt_object(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = "15.001,32.001"
        self.assertEqual(geo_pt_1, geo_pt_2)
        
    def test_is_not_equal_when_comparison_str_GeoPt_object(self):
        geo_pt_1 = fields.GeoPt("15.001,32.001")
        geo_pt_2 = "25.001,32.001"
        self.assertNotEqual(geo_pt_1, geo_pt_2)

    def test_compare_empty_GeoPt_to_None_object(self):
        geo_pt_1 = fields.GeoPt(None)
        geo_pt_2 = None
        self.assertEqual(geo_pt_1, geo_pt_2)
        
    def test_allows_GeoPt_instantiated_with_empty_string(self):
        geo_pt = fields.GeoPt("")
        self.assertEqual(None, geo_pt.lat)
        self.assertEqual(None, geo_pt.lon)

    def test_uses_empty_string_as_unicode_representation_for_empty_GeoPt(self):
        geo_pt = fields.GeoPt("")
        self.assertEqual("", force_str(geo_pt))

    def test_splits_geo_point_on_comma(self):
        pt = fields.GeoPt("15.001,32.001")
        self.assertEqual("15.001", str(pt.lat))
        self.assertEqual("32.001", str(pt.lon))

    def test_raises_error_when_attribute_error_on_split(self):
        class Fake(object):
            pass

        with self.assertRaises(exceptions.ValidationError):
            fields.GeoPt(Fake)

    def test_raises_error_when_type_error_on_split(self):
        with self.assertRaises(exceptions.ValidationError):
            x, y = fields.GeoPt("x,x")

    def test_returns_float_value_when_valid_value(self):
        geo_pt = fields.GeoPt("45.005,180")
        self.assertEqual(45.005, geo_pt.lat)

    def test_raises_exception_when_value_is_out_of_upper_range(self):
        with self.assertRaises(exceptions.ValidationError):
            fields.GeoPt("180,180")

    def test_raises_exception_when_value_is_out_of_lower_range(self):
        with self.assertRaises(exceptions.ValidationError):
            fields.GeoPt("-180,180")

    def test_len_returns_len_of_unicode_value(self):
        geo_pt = fields.GeoPt("84,12")
        self.assertEqual(9, len(geo_pt))

    def test_raises_exception_not_enough_values_to_unpack(self):
        with self.assertRaises(exceptions.ValidationError):
            fields.GeoPt("22")

    def test_raises_exception_too_many_values_to_unpack(self):
        with self.assertRaises(exceptions.ValidationError):
            fields.GeoPt("22,50,90")
