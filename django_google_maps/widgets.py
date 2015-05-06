from __future__ import unicode_literals

from django.forms import widgets


__all__ = ('GoogleMapsAddressWidget', 'GoogleMapsAddressInputWidget', 'GoogleMapsAddressTextareaWidget')


class GoogleMapsWidgetMixin(object):
    "Renders Google map after the field"

    class Media:
        css = {'all': ('django_google_maps/css/google-maps-admin.css', )}
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js',
            'https://maps.google.com/maps/api/js',
            'django_google_maps/js/google-maps-admin.js',
        )

    def _append_wrapper(self, to):
        return to + '<div class="map_canvas_wrapper"><div id="map_canvas"></div></div>'


class GoogleMapsAddressInputWidget(widgets.TextInput, GoogleMapsWidgetMixin):

    def render(self, *args, **kwargs):
        result = super(GoogleMapsAddressInputWidget, self).render(*args, **kwargs)
        return self._append_wrapper(result)


class GoogleMapsAddressTextareaWidget(widgets.Textarea, GoogleMapsWidgetMixin):

    def render(self, *args, **kwargs):
        result = super(GoogleMapsAddressTextareaWidget, self).render(*args, **kwargs)
        return self._append_wrapper(result)


# backwards compatibility
GoogleMapsAddressWidget = GoogleMapsAddressInputWidget
