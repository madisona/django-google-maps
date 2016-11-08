from django.db import models

from django_google_maps.fields import AddressField, GeoLocationField


class SampleModel(models.Model):
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(blank=True)

    def __str__(self):
        return self.address
