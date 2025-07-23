from django.db import models

from django_google_maps.fields import AddressField, GeoLocationField


class Location(models.Model):
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(blank=True)

    def __str__(self):
        return self.address


class Hotel(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class HotelLocation(models.Model):
    address = AddressField(max_length=100)
    geolocation = GeoLocationField(blank=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="locations")
