from django.conf.urls import url

from .views import slack_invite

urlpatterns = [
    url('^slack', slack_invite, name='invite'),
]
