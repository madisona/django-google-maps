from django.contrib import admin
from django.forms.widgets import TextInput

from django_google_maps.fields import AddressField, GeoLocationField
from django_google_maps.widgets import GoogleMapsAddressWidget
from sample import models


class SampleModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        AddressField: {'widget': GoogleMapsAddressWidget},
        GeoLocationField: {'widget': TextInput()},
    }


admin.site.register(models.SampleModel, SampleModelAdmin)
