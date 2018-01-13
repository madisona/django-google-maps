
import django
from django.contrib import admin
admin.autodiscover()


if django.get_version() >= '2.0.0':
    from django.urls import re_path as url
else:
    from django.conf.urls import url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
