from django import test
from django_google_maps.widgets import GoogleMapsAddressWidget


class WidgetTests(test.TestCase):

    def test_render_returns_xxxxxxx(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('name', 'value', attrs={'a1': 1, 'a2': 2})
        expected = '<input a1="1" a2="2" name="name" type="text" value="value" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertEqual(expected, results)

    def test_render_returns_blank_for_value_when_none(self):
        widget = GoogleMapsAddressWidget()
        results = widget.render('name', None, attrs={'a1': 1, 'a2': 2})
        expected = '<input a1="1" a2="2" name="name" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertEqual(expected, results)
