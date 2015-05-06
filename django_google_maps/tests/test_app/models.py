from django.db import models
from django_google_maps import fields


class Person(models.Model):
    address = fields.AddressField(max_length=100)
    geolocation = fields.GeoLocationField(blank=True)
