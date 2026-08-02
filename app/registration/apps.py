from django.apps import AppConfig
from django.contrib import admin


class RegistrationConfig(AppConfig):
    name = "app.registration"

    def ready(self):
        from .forms import AdminLoginForm

        admin.site.login_form = AdminLoginForm
