from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = (
    path('', include('landing.urls', namespace='landing')),
    path('', include('registration.urls', namespace='registration')),
    path('', include('slack.urls', namespace='slack')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('jobs/api/', include('jobs.api.v1.urls', namespace='jobs_api')),
    path('admin/', include(admin.site.urls)),
    path('markdown/', include('markdownx.urls')),
)

