from django.urls import include, path

from .views import CustomLoginView, index, register

app_name = "landing"

urlpatterns = (
    path("", index, name="landing"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register", register, name="register"),
    path("", include("django.contrib.auth.urls")),
)
