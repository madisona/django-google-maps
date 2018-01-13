from rest_framework import viewsets

from sample.api.serializers import SampleModelSerializer
from sample.models import SampleModel


class SampleViewSet(viewsets.ModelViewSet):
    model = SampleModel
    queryset = SampleModel.objects.all()
    serializer_class = SampleModelSerializer