import django
from django.contrib import admin

from sample import urls

admin.autodiscover()

if django.get_version() >= '2.0.0':
    from django.urls import re_path as url, include
else:
    from django.conf.urls import url

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(urls, namespace='api')),
]
