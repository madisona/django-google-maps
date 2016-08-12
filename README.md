Django-google-maps is a simple application that provides the basic
hooks into google maps V3 api for use in django models from django
version 1.3.

I'm using this to allow someone from the admin panels to type a
freeform address, have the address geocoded on change and plotted
on the map. If the location is not 100% correct, the user can
drag the marker to the correct spot and the geo coordinates will
update.

### Status
[![Build Status](https://travis-ci.org/madisona/django-google-maps.png)](https://travis-ci.org/madisona/django-google-maps)

USAGE:
------
- include the `django_google_maps` app in your `settings.py`
- Add your Google Maps API Key in your `settings.py` as `GOOGLE_MAPS_API_KEY`
- create a model that has both an address field and geolocation field
  <pre><code>
    from django.db import models
    from django_google_maps import fields as map_fields

    class Rental(models.Model):
        address = map_fields.AddressField(max_length=200)
        geolocation = map_fields.GeoLocationField(max_length=100)
  </code></pre>
- in the `admin.py` include the following as a formfield_override
  <pre><code>
      from django.contrib import admin
      from django_google_maps import widgets as map_widgets
      from django_google_maps import fields as map_fields

      class RentalAdmin(admin.ModelAdmin):
          formfield_overrides = {
              map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
          }
  </code></pre>

That should be all you need to get started. If you're not using Django 1.3
make sure that the static media is in a location that will be found and
properly served. The assumed location is `settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',`

I also like to make the geolocation field readonly in the admin so a user
(myself) doesn't accidentally change it to a nonsensical value. There is
validation on the field so you can't enter an incorrect value, but you could
enter something that is not even close to the address you intended.

When you're displaying the address back to the user, just request the map
using the geocoordinates that were saved in your model. Maybe sometime when
I get around to it I'll see if I can create a method that will build that
into the model.
