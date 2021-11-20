# The core of this module was adapted from Google AppEngine's
# GeoPt field, so I've included their copyright and license.
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from django.core import exceptions
from django.db import models
from django.utils.encoding import force_str

__all__ = ('AddressField', 'GeoLocationField')


def typename(obj):
    """Returns the type of obj as a string. More descriptive and specific than
    type(obj), and safe for any object, unlike __class__."""
    if hasattr(obj, '__class__'):
        return getattr(obj, '__class__').__name__
    else:
        return type(obj).__name__


class GeoPt(object):
    """A geographical point."""

    lat = None
    lon = None

    def __init__(self, lat, lon=None):
        """
        If the model field has 'blank=True' or 'null=True' then
        we can't always expect the GeoPt to be instantiated with
        a valid value. In this case we'll let GeoPt be instantiated
        as an empty item, and the string representation should be
        an empty string instead of 'lat,lon'.
        """
        if not lat:
            return

        if lon is None:
            lat, lon = self._split_geo_point(lat)
        self.lat = self._validate_geo_range(lat, 90)
        self.lon = self._validate_geo_range(lon, 180)

    def __str__(self):
        if self.lat is not None and self.lon is not None:
            return "%s,%s" % (self.lat, self.lon)
        return ''

    def __eq__(self, other):
        if isinstance(other, GeoPt):
            return bool(self.lat == other.lat and self.lon == other.lon)

    def __len__(self):
        return len(force_str(self))

    def _split_geo_point(self, geo_point):
        """splits the geo point into lat and lon"""
        try:
            lat, lon = geo_point.split(',')
            return lat, lon
        except (AttributeError, ValueError):
            m = 'Expected a "lat,long" formatted string; received %s (a %s).'
            raise exceptions.ValidationError(m % (geo_point,
                                                  typename(geo_point)))

    def _validate_geo_range(self, geo_part, range_val):
        try:
            geo_part = float(geo_part)
            if abs(geo_part) > range_val:
                m = 'Must be between -%s and %s; received %s'
                raise exceptions.ValidationError(m % (range_val, range_val,
                                                      geo_part))
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                'Expected float, received %s (a %s).' % (geo_part,
                                                         typename(geo_part)))
        return geo_part


class AddressField(models.CharField):
    pass


class GeoLocationField(models.CharField):
    """
    A geographical point, specified by floating-point latitude and longitude
    coordinates. Often used to integrate with mapping sites like Google Maps.
    May also be used as ICBM coordinates.

    This is the georss:point element. In XML output, the coordinates are
    provided as the lat and lon attributes. See: http://georss.org/

    Serializes to '<lat>,<lon>'. Raises BadValueError if it's passed an invalid
    serialized string, or if lat and lon are not valid floating points in the
    ranges [-90, 90] and [-180, 180], respectively.
    """
    description = "A geographical point, specified by floating-point latitude and longitude coordinates."

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(GeoLocationField, self).__init__(*args, **kwargs)

    def from_db_value(self, value, *args, **kwargs):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, GeoPt):
            return value
        return GeoPt(value)

    def get_prep_value(self, value):
        """prepare the value for database query"""
        if value is None:
            return None
        return force_str(self.to_python(value))

    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
