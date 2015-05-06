from __future__ import unicode_literals

from django.test import TestCase
from ..fields import GeoPt
from .test_app.models import Person


class GeoLocationFieldTests(TestCase):

    def test_getting_lat_lon_from_model_given_string(self):
        sut = Person(geolocation='45,90')
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_getting_lat_lon_from_model_given_pt(self):
        sut = Person(geolocation=GeoPt('45,90'))
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_getting_lat_lon_from_model_in_db_given_string(self):
        sut = Person.objects.create(geolocation='45,90')
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_exact_match_query(self):
        sut = Person.objects.create(geolocation='45,90')
        result = Person.objects.get(geolocation__exact=GeoPt('45,90'))
        self.assertEqual(result, sut)

    def test_in_match_query(self):
        sut = Person.objects.create(geolocation='45,90')
        result = Person.objects.get(geolocation__in=(GeoPt('45,90'),))
        self.assertEqual(result, sut)

    def test_raises_typeerror_for_unsupported_lookup(self):
        with self.assertRaises(TypeError):
            Person.objects.get(geolocation__iexact=GeoPt('45,90'))

    def test_value_to_string_with_point(self):
        sut = Person.objects.create(geolocation=GeoPt('45,90'))
        field = Person._meta.fields[-1]
        self.assertEqual('45.0,90.0', field.value_to_string(sut))

    def test_value_to_string_with_string(self):
        sut = Person.objects.create(geolocation='45,90')
        field = Person._meta.fields[-1]
        self.assertEqual('45.0,90.0', field.value_to_string(sut))

    def test_get_prep_value_returns_none_when_none(self):
        field = Person._meta.fields[-1]
        result = field.get_prep_value(None)
        self.assertEqual(None, result)
