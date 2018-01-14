from decimal import Decimal, InvalidOperation

from django.utils.translation import gettext as _
from rest_framework import serializers

from sample.models import SampleModel


def is_float(value: str):
    try:
        val = Decimal(value)
    except InvalidOperation:
        # Decimal("Cat") will raises this error
        return False
    else:
        return True


def lat_long_digits(value: str):
    if len(value.split(',')) != 2:
        raise serializers.ValidationError(_(f'Expect only 2 values'))
    try:
        [lat, long] = value.split(',')
        lat = lat.strip()
        long = long.strip()
    except ValueError:
        raise serializers.ValidationError(_(f'Need 2 values no more no less'))
    else:
        if is_float(lat) is False and is_float(long) is True:
            raise serializers.ValidationError(_(f'Latitude is not a digits'))
        elif is_float(lat) is True and is_float(long) is False:
            raise serializers.ValidationError(_(f'Longitude is not a digits'))
        elif is_float(lat) is False and is_float(long) is False:
            raise serializers.ValidationError(_(f'Latitude and Longitude are not a digits'))
        else:
            invalid_lat = Decimal("-90") > Decimal(lat) or Decimal(lat) > Decimal("90")
            invalid_long = Decimal("-180") > Decimal(long) or Decimal(long) > Decimal("180")
            if invalid_lat and (invalid_long is False):
                raise serializers.ValidationError(_(f'Latitude is valid in range (-90, 90)'))
            elif (invalid_lat is False) and invalid_long:
                raise serializers.ValidationError(_(f'Longitude is valid in range (-180, 180)'))
            elif invalid_lat and invalid_long:
                raise serializers.ValidationError(_(f'Latitude and Longitude are invalid'))


class SampleModelSerializer(serializers.ModelSerializer):
    geolocation = serializers.CharField(validators=[lat_long_digits])

    class Meta:
        model = SampleModel
        fields = [
            'address',
            'geolocation',
        ]
