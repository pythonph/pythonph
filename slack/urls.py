from django.urls import path

from .views import slack_invite


app_name = 'slack'

urlpatterns = [
    path('slack', slack_invite, name='invite'),
]
