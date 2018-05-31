import locale

from django import test
from django.conf import settings
from django_google_maps.widgets import GoogleMapsAddressWidget


class WidgetTests(test.TestCase):
    def setUp(self):
        if hasattr(settings, 'GOOGLE_MAPS_DEFAULT_LANGUAGE'):
            self.GOOGLE_MAPS_DEFAULT_LANGUAGE = settings.GOOGLE_MAPS_DEFAULT_LANGUAGE

        else:
            if locale.getdefaultlocale():
                self.GOOGLE_MAPS_DEFAULT_LANGUAGE = locale.getdefaultlocale()[0]
            else:
                self.GOOGLE_MAPS_DEFAULT_LANGUAGE = 'en'

    def test_render_returns_xxxxxxx(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('name', 'value', attrs={'a1': 1, 'a2': 2})
        expected = '<input a1="1" a2="2" name="name" type="text" value="value" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_render_returns_blank_for_value_when_none(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('name', None, attrs={'a1': 1, 'a2': 2})
        expected = '<input a1="1" a2="2" name="name" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_maps_js_uses_api_key_and_default_language(self):
        widget = GoogleMapsAddressWidget()
        google_maps_js = "https://maps.google.com/maps/api/js?key={}&libraries=places&language={}".format(
            settings.GOOGLE_MAPS_API_KEY,
            self.GOOGLE_MAPS_DEFAULT_LANGUAGE)
        self.assertEqual(google_maps_js, widget.Media().js[1])
