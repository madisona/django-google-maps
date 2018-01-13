"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from sample.api.serializers import SampleModelSerializer


class SimpleTest(TestCase):
    def test_geolocation_field_serializer(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': 'asb,aaa'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Latitude and Longitude are not a digits']} == instance.errors

    def test_wrong_comma_string(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': '10.12, asb,'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Expect only 2 values']} == instance.errors

    def test_lat_string(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': 'asb,100.12'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Latitude is not a digits']} == instance.errors

    def test_longitude_string(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': '10.12, cat'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Longitude is not a digits']} == instance.errors

    def test_outrange_latitude(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': '100.0,90.0'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Latitude is valid in range (-90, 90)']} == instance.errors

    def test_outrange_longitude(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': '15.52,190.0'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Longitude is valid in range (-180, 180)']} == instance.errors

    def test_outrage_bot_latitude_and_longitude(self):
        instance = SampleModelSerializer(
            data={
                'address': 'some where',
                'geolocation': '-200,-190.0'
            })
        assert False is instance.is_valid()
        assert {'geolocation': ['Latitude and Longitude are invalid']} == instance.errors
