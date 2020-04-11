from django.conf.urls import url

from .views import index, post

urlpatterns = (
    url(r'^$', index, name='jobs'),
    url(r'^post$', post, name='jobs_post'),
)

