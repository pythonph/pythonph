from django.contrib.auth import authenticate, get_user_model
from django.test import TestCase
from django.urls import reverse

from .backends import EmailBackend
from .forms import LoginForm, UserCreationForm

User = get_user_model()

PASSWORD = "Str0ng!Passw0rd"


class EmailBackendTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="juan",
            email="juan@example.com",
            password=PASSWORD,
            first_name="Juan",
            last_name="Dela Cruz",
        )

    def test_authenticate_with_email(self):
        user = authenticate(username="juan@example.com", password=PASSWORD)
        self.assertEqual(user, self.user)

    def test_authenticate_with_email_is_case_insensitive(self):
        user = authenticate(username="JUAN@Example.COM", password=PASSWORD)
        self.assertEqual(user, self.user)

    def test_authenticate_rejects_wrong_password(self):
        user = authenticate(username="juan@example.com", password="wrong")
        self.assertIsNone(user)

    def test_authenticate_rejects_username(self):
        user = authenticate(username="juan", password=PASSWORD)
        self.assertIsNone(user)

    def test_authenticate_rejects_missing_credentials(self):
        self.assertIsNone(authenticate(username=None, password=None))
        self.assertIsNone(authenticate(username="juan@example.com", password=None))

    def test_backend_get_user(self):
        backend = EmailBackend()
        self.assertEqual(backend.get_user(self.user.pk), self.user)
        self.assertIsNone(backend.get_user(999999))


class UserCreationFormTests(TestCase):
    def test_register_form_generates_username(self):
        form = UserCreationForm(
            data={
                "first_name": "Maria",
                "last_name": "Santos",
                "email": "Maria@Example.com",
                "password1": PASSWORD,
                "password2": PASSWORD,
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        user = form.save()
        self.assertEqual(user.email, "maria@example.com")
        # A non-empty username is auto-generated from the email.
        self.assertTrue(user.username)
        self.assertNotIn("@", user.username)

    def test_register_form_rejects_duplicate_email_case_insensitive(self):
        User.objects.create_user(username="existing", email="existing@example.com", password=PASSWORD)
        form = UserCreationForm(
            data={
                "first_name": "Other",
                "last_name": "Person",
                "email": "EXISTING@Example.com",
                "password1": PASSWORD,
                "password2": PASSWORD,
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_login_form_uses_email_field(self):
        form = LoginForm()
        self.assertEqual(form.fields["username"].label, "Email address")


class RegistrationViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="juan",
            email="juan@example.com",
            password=PASSWORD,
            first_name="Juan",
            last_name="Dela Cruz",
        )

    def test_login_page_uses_email_label(self):
        response = self.client.get(reverse("registration:login"))
        self.assertContains(response, "Email address")
        self.assertNotContains(response, ">Username<")

    def test_register_page_has_no_username_field(self):
        response = self.client.get(reverse("registration:register"))
        self.assertNotContains(response, 'name="username"')
        self.assertContains(response, "Email address")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")

    def test_login_with_email_authenticates(self):
        response = self.client.post(
            reverse("registration:login"),
            {"username": "JUAN@example.com", "password": PASSWORD},
            follow=True,
        )
        self.assertTrue(response.context["user"].is_authenticated)

    def test_login_with_username_is_rejected(self):
        response = self.client.post(
            reverse("registration:login"),
            {"username": "juan", "password": PASSWORD},
            follow=True,
        )
        self.assertFalse(response.context["user"].is_authenticated)

    def test_register_creates_user(self):
        response = self.client.post(
            reverse("registration:register"),
            {
                "first_name": "Ana",
                "last_name": "Reyes",
                "email": "ana@example.com",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(email__iexact="ana@example.com").exists())

    def test_register_rejects_duplicate_email(self):
        response = self.client.post(
            reverse("registration:register"),
            {
                "first_name": "Other",
                "last_name": "Person",
                "email": "juan@example.com",
                "password1": PASSWORD,
                "password2": PASSWORD,
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already exists")

    def test_logout_requires_post(self):
        self.client.login(username="juan@example.com", password=PASSWORD)
        response = self.client.get(reverse("registration:logout"))
        self.assertEqual(response.status_code, 405)

    def test_logout_post_logs_out(self):
        self.client.login(username="juan@example.com", password=PASSWORD)
        response = self.client.post(reverse("registration:logout"), follow=True)
        self.assertFalse(response.context["user"].is_authenticated)


class AdminLoginFormTests(TestCase):
    def test_admin_login_uses_email_label(self):
        response = self.client.get("/admin/login/")
        self.assertContains(response, "Email address")
        self.assertNotContains(response, ">Username<")
