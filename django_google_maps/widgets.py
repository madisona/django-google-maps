import locale

from django.conf import settings
from django.forms import widgets

if hasattr(settings, 'GOOGLE_MAPS_DEFAULT_LANGUAGE'):
    GOOGLE_MAPS_DEFAULT_LANGUAGE = settings.GOOGLE_MAPS_DEFAULT_LANGUAGE

else:
    if locale.getdefaultlocale():
        GOOGLE_MAPS_DEFAULT_LANGUAGE = locale.getdefaultlocale()[0]

    else:
        GOOGLE_MAPS_DEFAULT_LANGUAGE = 'en'


class GoogleMapsAddressWidget(widgets.TextInput):
    """a widget that will place a google map right after the #id_address field"""
    template_name = "django_google_maps/widgets/map_widget.html"

    class Media:
        css = {
            'all': (settings.STATIC_URL +
                    'django_google_maps/css/google-maps-admin.css', )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js',
            'https://maps.google.com/maps/api/js?key={}&libraries=places&language={}'.format(
                settings.GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_DEFAULT_LANGUAGE),
            settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
        )
