from django.urls import include, path

from .api_urls import urlpatterns as api_patterns
from .views import index, post

app_name = "jobs"

urlpatterns = [
    path("", index, name="index"),
    path("api/v1/", include(api_patterns)),
    path("post", post, name="post"),
]
