import django
from django.conf import settings
from django.forms import widgets

# Check if we're on Django 5.2+
USE_SCRIPT_OBJECT = django.VERSION >= (5, 2)

if USE_SCRIPT_OBJECT:
    from django.forms.widgets import Script


class GoogleMapsAddressWidget(widgets.TextInput):
    """a widget that will place a google map right after the #id_address field"""

    template_name = "django_google_maps/widgets/map_widget.html"

    class Media:
        css = {"all": ("django_google_maps/css/google-maps-admin.css",)}

        if USE_SCRIPT_OBJECT:
            js = (
                Script(
                    f'https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_MAPS_API_KEY}&loading=async&callback=initGoogleMap',  # noqa: E501
                    **{
                        "async": True,
                    }),
                'django_google_maps/js/google-maps-admin.js',
            )
        else:
            js = (
                f"https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_MAPS_API_KEY}&loading=async&callback=initGoogleMap",  # noqa: E501
                'django_google_maps/js/google-maps-admin.js',
            )
