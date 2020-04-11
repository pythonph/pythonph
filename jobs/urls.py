from django.conf.urls import include
from django.urls import path

from .views import index, post
from .api import v1 as api_v1


app_name = 'jobs'

urlpatterns = (
    path('', index, name='jobs'),
    path('api', include(api_v1.urls)),
    path('post', post, name='jobs_post'),
)
