import jobs
import landing
import registration
import slack
from django.conf.urls import include, patterns, url
from django.contrib import admin

urlpatterns = patterns(
    '',
    url(r'', include(landing.urls)),
    url(r'', include(registration.urls)),
    url(r'', include(slack.urls)),
    url(r'^jobs/', include(jobs.urls)),
    url(r'^jobs/api/', include(jobs.api.v1.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^markdown/', include('django_markdown.urls')),
)

