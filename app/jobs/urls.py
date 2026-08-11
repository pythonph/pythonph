from django.urls import include, path

from .api_urls import urlpatterns as api_patterns
from .views import companies, index, job_detail, post

app_name = "jobs"

urlpatterns = [
    path("", index, name="index"),
    path("api/v1/", include(api_patterns)),
    path("companies/", companies, name="companies"),
    path("job/<int:pk>/", job_detail, name="job_detail"),
    path("post", post, name="post"),
]
