from django.conf.urls import include, url

urlpatterns = [
    url('^slack', 'slack.views.slack_invite', name='invite'),
]
