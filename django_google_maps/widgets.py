
from django.conf import settings
from django.forms import widgets
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe
from django.forms.util import flatatt

class GoogleMapsAddressWidget(widgets.TextInput):
    "a widget that will place a google map right after the #id_address field"
    
    class Media:
        css = {'all': (settings.STATIC_URL + 'django_google_maps/css/google-maps-admin.css',),}
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            'https://maps.google.com/maps/api/js?sensor=false',
            settings.STATIC_URL + 'django_google_maps/js/google-maps-admin.js',
        )

    def render(self, name, value, attrs=None):
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)

        addr_type = 'default'
        if (settings.DJANGO_GOOGLE_MAPS['ADDRESS_TYPE'] and settings.DJANGO_GOOGLE_MAPS['ADDRESS_TYPE'] in ['default', 'simple']):
            addr_type = settings.DJANGO_GOOGLE_MAPS['ADDRESS_TYPE']

        if value != '':
            # Only add the 'value' attribute if a value is non-empty.
            final_attrs['value'] = force_unicode(self._format_value(value))
        return mark_safe(u'<input%s data-addrtype="%s"/><div class="map_canvas_wrapper"><div id="map_canvas"></div></div>' % (flatatt(final_attrs), addr_type))
