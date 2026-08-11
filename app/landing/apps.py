from django.apps import AppConfig
from django.contrib import admin


class LandingConfig(AppConfig):
    name = "app.landing"

    def ready(self):
        from .forms import AdminLoginForm

        admin.site.login_form = AdminLoginForm
