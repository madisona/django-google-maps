from django import forms
from django.db import models
from django.test import TestCase

from django_google_maps.fields import GeoPt, GeoLocationField


class GeoLocationFieldHasChangedTests(TestCase):
    """
    Integration tests for the has_changed functionality with forms.
    """

    def setUp(self):
        """Set up a model and form for testing."""

        class TestModel(models.Model):
            location = GeoLocationField(max_length=100, blank=True)

            class Meta:
                app_label = "django_google_maps"

        self.TestModel = TestModel

        # Create a form for testing
        class TestForm(forms.ModelForm):
            class Meta:
                model = TestModel
                fields = ["location"]

        self.TestForm = TestForm

    def test_has_changed_false_when_same_value(self):
        """
        Test that has_changed returns False when the value hasn't actually changed.
        This is the main bug that was fixed.
        """
        # Create a GeoPt object (simulating initial data from database)
        initial_value = GeoPt(40.7128, -74.0060)

        # Create form data (simulating form submission with same value)
        form_data = {"location": "40.7128,-74.0060"}

        # Create form with initial data
        form = self.TestForm(data=form_data, initial={"location": initial_value})

        # The field should not be marked as changed
        self.assertFalse(form.has_changed())
        self.assertNotIn("location", form.changed_data)

    def test_has_changed_true_when_value_actually_changed(self):
        """
        Test that has_changed returns True when the value has actually changed.
        """
        # Create a GeoPt object (simulating initial data from database)
        initial_value = GeoPt(40.7128, -74.0060)

        # Create form data with different coordinates
        form_data = {"location": "41.0000,-73.0000"}

        # Create form with initial data
        form = self.TestForm(data=form_data, initial={"location": initial_value})

        # The field should be marked as changed
        self.assertTrue(form.has_changed())
        self.assertIn("location", form.changed_data)

    def test_has_changed_false_with_empty_values(self):
        """
        Test that has_changed handles empty values correctly.
        """
        # Test empty initial and empty form data
        form_data = {"location": ""}
        form = self.TestForm(data=form_data, initial={"location": None})

        self.assertFalse(form.has_changed())
        self.assertNotIn("location", form.changed_data)

    def test_has_changed_true_from_empty_to_value(self):
        """
        Test that has_changed returns True when going from empty to a value.
        """
        # Empty initial, non-empty form data
        form_data = {"location": "40.7128,-74.0060"}
        form = self.TestForm(data=form_data, initial={"location": None})

        self.assertTrue(form.has_changed())
        self.assertIn("location", form.changed_data)

    def test_has_changed_true_from_value_to_empty(self):
        """
        Test that has_changed returns True when going from a value to empty.
        """
        # Non-empty initial, empty form data
        initial_value = GeoPt(40.7128, -74.0060)
        form_data = {"location": ""}
        form = self.TestForm(data=form_data, initial={"location": initial_value})

        self.assertTrue(form.has_changed())
        self.assertIn("location", form.changed_data)

    def test_widget_has_changed_method(self):
        """
        Test the widget's has_changed method directly.
        """
        # Get the field from the form
        form = self.TestForm()
        field = form.fields["location"]
        widget = field.widget

        # Test the widget's has_changed method directly
        initial_geopt = GeoPt(40.7128, -74.0060)
        same_string = "40.7128,-74.0060"
        different_string = "41.0000,-73.0000"

        # If using custom widget, test its has_changed method
        if hasattr(widget, "has_changed"):
            self.assertFalse(widget.has_changed(initial_geopt, same_string))
            self.assertTrue(widget.has_changed(initial_geopt, different_string))
