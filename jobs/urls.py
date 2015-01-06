import frontend
from api.v1 import api
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'^$', include(frontend.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(api.urls)),
)

