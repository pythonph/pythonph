import re
import secrets

from django import forms
from django.contrib.admin.forms import AdminAuthenticationForm
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    """Registration form that uses email as the primary credential.

    A unique ``username`` is generated automatically from the email address
    so Django's default ``User`` model keeps working without exposing a
    username field to the user.
    """

    first_name = forms.CharField(max_length=30, label="First name")
    last_name = forms.CharField(max_length=150, label="Last name")
    email = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]

    def clean_email(self):
        email = self.cleaned_data.get("email", "").strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email address already exists.")
        return email

    def _generate_username(self):
        base = re.sub(r"[^a-zA-Z0-9_.]+", "", self.cleaned_data["email"].split("@")[0])
        base = (base or "user")[:30]
        username = base
        while User.objects.filter(username__iexact=username).exists():
            username = f"{base[:26]}_{secrets.token_hex(2)}"
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self._generate_username()
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    """Login form that lets users sign in with their email address."""

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )


class AdminLoginForm(AdminAuthenticationForm):
    """Admin login form labelled with email instead of username."""

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autofocus": True}),
    )
