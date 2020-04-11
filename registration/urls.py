from django.conf.urls import include, url

from .views import register

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^register', register, name='register'),
]
