from django import test
from django.conf import settings

from django_google_maps import widgets


class WidgetTests(test.TestCase):
    def test_render_returns_with_value(self):
        widget = widgets.GoogleMapsAddressWidget()
        results = widget.render("name", "value", attrs={"a1": 1, "a2": 2})
        expected = '<input a1="1" a2="2" name="name" type="text" value="value" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_render_returns_blank_for_value_when_none(self):
        widget = widgets.GoogleMapsAddressWidget()
        results = widget.render("name", None, attrs={"a1": 1, "a2": 2})
        expected = '<input a1="1" a2="2" name="name" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_widgets_media_js(self):
        widget = widgets.GoogleMapsAddressWidget()
        google_maps_js = (
            "https://maps.google.com/maps/api/js?key={}&libraries=places".format(
                settings.GOOGLE_MAPS_API_KEY
            )
        )
        admin_js = "django_google_maps/js/google-maps-admin.js"
        self.assertEqual(google_maps_js, widget.Media().js[1])
        self.assertEqual(admin_js, widget.Media().js[2])

    def test_template_used(self):
        widget = widgets.GoogleMapsAddressWidget()
        self.assertEqual(
            widget.template_name,
            "django_google_maps/widgets/map_widget.html",
        )


class InlineWidgetTests(test.TestCase):
    def test_render_returns_with_value(self):
        widget = widgets.GoogleMapsAddressInlineWidget()
        results = widget.render("locations-0-address", "New York", attrs={"attr1": 1})
        expected = '<input attr1="1" name="locations-0-address" type="text" value="New York" />'
        expected += '<div class="map_canvas_wrapper"><div id="locations-0-address_map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_render_returns_blank_for_value_when_none(self):
        widget = widgets.GoogleMapsAddressInlineWidget()
        results = widget.render("locations-1-address", None, attrs={"a1": 1, "a2": 2})
        expected = '<input a1="1" a2="2" name="locations-1-address" type="text" />'
        expected += '<div class="map_canvas_wrapper">'
        expected += '<div id="locations-1-address_map_canvas"></div></div>'
        self.assertHTMLEqual(expected, results)

    def test_widgets_media_js(self):
        widget = widgets.GoogleMapsAddressInlineWidget()
        google_maps_js = (
            "https://maps.google.com/maps/api/js?key={}&libraries=places".format(
                settings.GOOGLE_MAPS_API_KEY
            )
        )
        admin_js = "django_google_maps/js/google-maps-admin-inline.js"
        self.assertEqual(google_maps_js, widget.Media().js[1])
        self.assertEqual(admin_js, widget.Media().js[2])

    def test_template_used(self):
        widget = widgets.GoogleMapsAddressInlineWidget()
        self.assertEqual(
            widget.template_name,
            "django_google_maps/widgets/map_widget_inline.html",
        )
