from django import test
from django_google_maps.tests.test_app import models
from django_google_maps.fields import GeoPt


class GeoLocationFieldTests(test.TestCase):

    def test_getting_lat_lon_from_model_given_string(self):
        sut_create = models.Person.objects.create(geolocation='45,90')
        sut = models.Person.objects.get(pk=sut_create.pk)
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_getting_lat_lon_from_model_given_pt(self):
        sut_create = models.Person.objects.create(geolocation=GeoPt('45,90'))
        sut = models.Person.objects.get(pk=sut_create.pk)
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_getting_lat_lon_from_model_in_db_given_string(self):
        sut_create = models.Person.objects.create(geolocation='45,90')
        sut = models.Person.objects.get(pk=sut_create.pk)
        self.assertEqual(45, sut.geolocation.lat)
        self.assertEqual(90, sut.geolocation.lon)

    def test_exact_match_query(self):
        sut = models.Person.objects.create(geolocation='45,90')
        result = models.Person.objects.get(geolocation__exact=GeoPt('45,90'))
        self.assertEqual(result, sut)

    def test_in_match_query(self):
        sut = models.Person.objects.create(geolocation='45,90')
        result = models.Person.objects.get(geolocation__in=(GeoPt('45,90'),))
        self.assertEqual(result, sut)

    def test_value_to_string_with_point(self):
        sut = models.Person.objects.create(geolocation=GeoPt('45,90'))
        field = models.Person._meta.fields[-1]
        self.assertEqual('45.0,90.0', field.value_to_string(sut))

    def test_value_to_string_with_string(self):
        sut = models.Person.objects.create(geolocation='45,90')
        field = models.Person._meta.fields[-1]
        self.assertEqual('45.0,90.0', field.value_to_string(sut))

    def test_get_prep_value_returns_none_when_none(self):
        field = models.Person._meta.fields[-1]
        result = field.get_prep_value(None)
        self.assertEqual(None, result)
