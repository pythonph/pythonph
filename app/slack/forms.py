from django import forms


class SlackInviteForm(forms.Form):
    email = forms.EmailField(label="Email")

