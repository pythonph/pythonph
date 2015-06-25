from django.conf.urls import include, url

urlpatterns = [
    url('^', include('django.contrib.auth.urls')),
    url('^register', 'registration.views.register', name='register'),
]
