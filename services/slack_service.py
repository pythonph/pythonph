"""Slack integration service for pythonph.

Replaces the inline notify_slack utility with a service class,
following the pythonasia services/ pattern.
"""

import requests
from django.conf import settings


class SlackService:
    """Thin wrapper around Slack's chat.postMessage API."""

    @staticmethod
    def notify(text: str, channel: str) -> None:
        """Post a message to a Slack channel.

        Skips sending in DEBUG mode.
        """
        if settings.DEBUG:
            return
        requests.post(
            "https://slack.com/api/chat.postMessage",
            data={
                "token": settings.SLACK_API_TOKEN,
                "channel": channel,
                "text": text,
                "username": "payton",
                "icon_emoji": ":snake:",
            },
        ).raise_for_status()
