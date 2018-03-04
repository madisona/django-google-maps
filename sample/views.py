from django.views.generic import FormView

from sample.forms import SampleForm


class SampleFormView(FormView):
    form_class = SampleForm
    template_name = "sample/index.html"
