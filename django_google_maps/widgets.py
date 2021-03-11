from django.conf import settings
from django.forms import widgets
from django.utils import translation

class GoogleMapsAddressWidget(widgets.TextInput):
    """a widget that will place a google map right after the #id_address field"""
    template_name = "django_google_maps/widgets/map_widget.html"

    def render(self, name, value, attrs=None, renderer=None):
        """
        Render the widget as an HTML string.
        I overwrote that, due to dynamic language change
        """
        output = super().render(name, value, attrs, renderer)
        output += '<script src="https://maps.google.com/maps/api/js?language={}&key={}&libraries=places"></script>'.format(
            translation.get_language(), settings.GOOGLE_MAPS_API_KEY
        )
        return output

    class Media:
        css = {
            'all': (settings.STATIC_URL +
                    'django_google_maps/css/google-maps-admin.css', )
        }
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js',
            # 'https://maps.google.com/maps/api/js?language={}&key={}&libraries=places'.format(
            #     settings.LANGUAGE_CODE, settings.GOOGLE_MAPS_API_KEY
            # ),
            settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
        )
