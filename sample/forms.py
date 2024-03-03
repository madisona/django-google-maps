from django import forms

from django_google_maps import widgets
from sample import models


class LocationForm(forms.ModelForm):
    class Meta(object):
        model = models.Location
        fields = ["address", "geolocation"]
        widgets = {"address": widgets.GoogleMapsAddressWidget}


class HotelLocationForm(forms.ModelForm):
    class Meta(object):
        model = models.HotelLocation
        fields = ["address", "geolocation", "hotel"]
        widgets = {
            "address": widgets.GoogleMapsAddressInlineWidget,
            "geolocation": forms.widgets.TextInput(attrs={"readonly": "readonly"}),
        }
