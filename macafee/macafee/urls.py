from django.conf.urls import include, url
from django.contrib import admin
from tweets import urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tweets/', include(urls))
]
