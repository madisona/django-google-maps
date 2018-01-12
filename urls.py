from django.urls import path

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'google_maps.views.home', name='home'),
    # path(r'google_maps/', google_maps.foo.urls),

    # Uncomment the admin/doc line below to enable admin documentation:
    # path(r'admin/doc/', django.contrib.admindocs.urls),

    # Uncomment the next line to enable the admin:
    path(r'admin/', admin.site.urls),
]
