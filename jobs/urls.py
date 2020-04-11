from django.urls import path

from .views import index, post


app_name = 'jobs'

urlpatterns = (
    path('', index, name='jobs'),
    path('post', post, name='jobs_post'),
)

