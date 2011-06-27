from django.db import models
from django.core import exceptions

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

    def __unicode__(self):
        if self.lat is not None and self.lon is not None:
            return "%s,%s" % (self.lat, self.lon)
        return ''

    def __len__(self):
        return len(self.__unicode__())

    def _split_geo_point(self, geo_point):
        """splits the geo point into lat and lon"""
        try:
            return geo_point.split(',')
        except (AttributeError, ValueError):
            raise exceptions.ValidationError(
                'Expected a "lat,long" formatted string; received %s (a %s).' %
            (geo_point, typename(geo_point)))

    def _validate_geo_range(self, geo_part, range_val):
        try:
            geo_part = float(geo_part)
            if abs(geo_part) > range_val:
                raise exceptions.ValidationError(
                'Must be between -%s and %s; received %s' % (range_val, range_val, geo_part)
            )
        except (TypeError, ValueError):
            raise exceptions.ValidationError(
                'Expected float, received %s (a %s).' % (geo_part, typename(geo_part))
            )
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
    __metaclass__ = models.SubfieldBase

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super(GeoLocationField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if isinstance(value, GeoPt):
            return value
        return GeoPt(value)

    def get_prep_value(self, value):
        """prepare the value for database query"""
        return unicode(value)

    def get_prep_lookup(self, lookup_type, value):
        # We only handle 'exact' and 'in'. All others are errors.
        if lookup_type == 'exact':
            return self.get_prep_value(value)
        elif lookup_type == 'in':
            return [self.get_prep_value(v) for v in value]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^django_google_maps\.fields\.GeoLocationField"])
    add_introspection_rules([], ["^django_google_maps\.fields\.AddressField"])
except ImportError:
    pass
