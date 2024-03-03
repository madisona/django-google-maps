from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps.fields import AddressField, GeoLocationField
from django_google_maps.widgets import GoogleMapsAddressWidget
from sample import forms, models


class LocationAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {"widget": GoogleMapsAddressWidget},
        GeoLocationField: {"widget": TextInput(attrs={"readonly": "readonly"})},
    }


class HotelLocationInlineAdmin(admin.StackedInline):
    model = models.HotelLocation
    form = forms.HotelLocationForm
    extra = 1


class HotelAdmin(admin.ModelAdmin):
    list_display = ["name"]
    inlines = [HotelLocationInlineAdmin]


admin.site.register(models.Location, LocationAdmin)
admin.site.register(models.Hotel, HotelAdmin)
