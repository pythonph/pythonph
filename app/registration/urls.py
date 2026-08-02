from django.urls import include, path

from .views import CustomLoginView, register

app_name = "registration"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("register", register, name="register"),
    path("", include("django.contrib.auth.urls")),
]
