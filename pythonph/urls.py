from django.conf.urls import include
from django.urls import path
from django.contrib import admin

urlpatterns = (
    path('', include('landing.urls', namespace='landing')),
    path('', include('registration.urls', namespace='registration')),
    path('', include('slack.urls', namespace='slack')),
    path('jobs/', include('jobs.urls', namespace='jobs')),
    path('admin/', admin.site.urls, name='admin'),
    path('markdown/', include('markdownx.urls')),
)

