``django-google-maps`` is a simple application that provides the basic
hooks into google maps V3 api for use in Django models from Django
version 1.11+.

Starting with ``django-google-maps`` version (0.7.0), Django 1.11+ is
required because Django changed their widget template rendering system.
Version 0.8.0 supports Django 2.0+, and as such removes support for
Python 2.7

I’m using this to allow someone from the admin panels to type a freeform
address, have the address geocoded on change and plotted on the map. If
the location is not 100% correct, the user can drag the marker to the
correct spot and the geo coordinates will update.

Status
~~~~~~

|Build Status|

USAGE:
------

-  include the ``django_google_maps`` app in your ``settings.py``

-  Add your Google Maps API Key in your ``settings.py`` as
   ``GOOGLE_MAPS_API_KEY``

-  create a model that has both an address field and geolocation field

   .. code:: python

      from django.db import models
      from django_google_maps import fields as map_fields

      class Rental(models.Model):
          address = map_fields.AddressField(max_length=200)
          geolocation = map_fields.GeoLocationField(max_length=100)

-  in the ``admin.py`` include the following as a formfield_override

   .. code:: python

      from django.contrib import admin
      from django_google_maps import widgets as map_widgets
      from django_google_maps import fields as map_fields

      class RentalAdmin(admin.ModelAdmin):
          formfield_overrides = {
              map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
          }

-  To change the map type (``hybrid`` by default), you can add an html
   attribute on the ``AddressField`` widget. The list of allowed values
   is: ``hybrid``, ``roadmap``, ``satellite``, ``terrain``

   .. code:: python

      from django.contrib import admin
      from django_google_maps import widgets as map_widgets
      from django_google_maps import fields as map_fields

      class RentalAdmin(admin.ModelAdmin):
          formfield_overrides = {
              map_fields.AddressField: {
                'widget': map_widgets.GoogleMapsAddressWidget(attrs={'data-map-type': 'roadmap'})},
          }

-  To change the autocomplete options, you can add an html attribute on
   the ``AddressField`` widget. See
   https://developers.google.com/maps/documentation/javascript/places-autocomplete#add_autocomplete
   for a list of available options

   .. code:: python

      import json from django.contrib import admin
      from django_google_maps import widgets as map_widgets
      from django_google_maps import fields as map_fields

      class RentalAdmin(admin.ModelAdmin): formfield_overrides = {
          map_fields.AddressField: { ‘widget’:
          map_widgets.GoogleMapsAddressWidget(attrs={
            ‘data-autocomplete-options’: json.dumps({ ‘types’: [‘geocode’,
            ‘establishment’], ‘componentRestrictions’: {
                        'country': 'us'
                    }
                })
            })
          },
      }

USING INLINE FORMS:
===================
-  To use as a model admin inline form, everything is basically the same as above except for the widget
   used. It's best to use ``django.contrib.admin.StackedInline`` as opposed to ``django.contrib.admin.TabularInline``

   .. code:: python

      from django.db import models
      from django_google_maps import fields as map_fields

      class Shipment(models.Model):
          tracking_id = models.CharField(max_length=255)
          carrier = models.CharField(max_length=255)

      class Location(models.Model):
          shipment = models.ForeignKey(Shipment)
          address = map_fields.AddressField(max_length=200)
          geolocation = map_fields.GeoLocationField(max_length=50)

-  in the ``admin.py`` file, define a model form and a stacked inline like below:

   .. code:: python

      from django import forms
      from django.contrib import admin
      from django_google_maps import widgets as map_widgets

      from . import models

      class LocationForm(forms.ModelForm):
          class Meta:
              model = models.Location
              widgets = {
                  "address": map_widgets.GoogleMapsAddressInlineWidget(),
              }

      class LocationInline(admin.StackedInline):
          model = models.Location
          form = LocationForm

      @admin.register(models.Shipment)
      class ShipmentAdmin(admin.ModelAdmin):
          inlines = [LocationInline]

That should be all you need to get started.

I also like to make the geolocation field readonly in the admin so a user
(myself) doesn't accidentally change it to a nonsensical value. There is
validation on the field so you can't enter an incorrect value, but you could
enter something that is not even close to the address you intended.

When you're displaying the address back to the user, just request the map
using the geocoordinates that were saved in your model. Maybe sometime when
I get around to it I'll see if I can create a method that will build that
into the model.

.. |Build Status| image:: https://travis-ci.org/madisona/django-google-maps.png
   :target: https://travis-ci.org/madisona/django-google-maps
