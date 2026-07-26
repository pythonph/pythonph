from django.urls import include, path

from .views import register

app_name = "registration"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("register", register, name="register"),
]
