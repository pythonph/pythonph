import requests
from django.conf import settings
from django.shortcuts import redirect, render
from django.utils.translation import ugettext as _
from slack.forms import SlackInviteForm

MISSING_SCOPE_ERROR_TEXT = """Missing admin scope: The token you provided is for
an account that is not an admin. You must provide a token from an admin account
in order to invite users through the Slack API."""

ALREADY_INVITED_ERROR_TEXT = """You have already been invited to Slack.  Check
for an email from feedback@slack.com."""


def slack_invite(request):
    if request.method == 'POST':
        form = SlackInviteForm(request.POST)
        if form.is_valid():
            res = requests.post(
                "https://{}.slack.com/api/users.admin.invite".format(
                    settings.SLACK_ORG,
                ),
                data={
                    'email': form.cleaned_data['email'],
                    'token': settings.SLACK_API_TOKEN,
                },
            )
            body = res.json()
            ok = body['ok']
            if ok:
                pass
            else:
                error = body['error']
                if error == 'missing_scope':
                    error_text = MISSING_SCOPE_ERROR_TEXT
                elif error == 'already_invited':
                    error_text = ALREADY_INVITED_ERROR_TEXT
                elif error == 'already_in_team':
                    return redirect('https://{}.slack.com'.format(
                        settings.SLACK_ORG,
                    ))
                else:
                    error_text = error
                form.add_error(None, _(error_text))
    else:
        form = SlackInviteForm()
    return render(request, 'slack/invite.html', {'form': form})
