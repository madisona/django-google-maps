from django import test
from django.conf import settings
from django_google_maps.widgets import GoogleMapsAddressWidget


class WidgetTests(test.TestCase):
    def test_render_returns_xxxxxxx(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render("name", "value", attrs={"a1": 1, "a2": 2})
        expected = '<div class="map_widget_wrapper">'
        expected += '<input a1="1" a2="2" name="name" type="text" value="value" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        expected += '<div id="map_message_box" role="alert"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_render_returns_blank_for_value_when_none(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render("name", None, attrs={"a1": 1, "a2": 2})
        expected = '<div class="map_widget_wrapper">'
        expected += '<input a1="1" a2="2" name="name" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        expected += '<div id="map_message_box" role="alert"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_maps_js_uses_api_key(self):
        widget = GoogleMapsAddressWidget()
        google_maps_js = (
            f"https://maps.googleapis.com/maps/api/js?key={settings.GOOGLE_MAPS_API_KEY}&loading=async&callback=initGoogleMap"  # noqa: E501
        )
        self.assertEqual(google_maps_js, widget.Media().js[0])
