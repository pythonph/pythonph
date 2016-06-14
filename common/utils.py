import requests
from django.conf import settings


def notify_slack(text, channel):
    if settings.DEBUG:
        return
    requests.post(
        'https://slack.com/api/chat.postMessage',
        data={
            'token': settings.SLACK_API_TOKEN,
            'channel': channel,
            'text': text,
            'username': "payton",
            'icon_emoji': ':snake:',
        },
    ).raise_for_status()
