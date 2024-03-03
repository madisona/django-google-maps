from django.views.generic import FormView

from sample.forms import LocationForm


class LocationFormView(FormView):
    form_class = LocationForm
    template_name = "sample/index.html"
