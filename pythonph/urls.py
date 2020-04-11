from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = (
    url(r'', include('landing.urls', namespace='landing')),
    url(r'', include('registration.urls', namespace='registration')),
    url(r'', include('slack.urls', namespace='slack')),
    url(r'^jobs/', include('jobs.urls', namespace='jobs')),
    url(r'^jobs/api/', include('jobs.api.v1.urls', namespace='jobs_api')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include('markdownx.urls')),
)

