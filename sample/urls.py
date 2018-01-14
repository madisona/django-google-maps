from rest_framework import routers

from sample.api.viewsets import SampleViewSet

app_name = 'api'
router = routers.SimpleRouter()
router.register(r'sample', SampleViewSet)
urlpatterns = router.urls
