from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthChangelistAddButtonTests(TestCase):
    """Unfold only renders the changelist add button for admins that set
    ``show_add_link`` (see ``unfold/helpers/add_link.html``). Django's stock
    User/Group admins don't, so the unfold mixins in ``app.accounts.admin``
    must keep the button visible."""

    @classmethod
    def setUpTestData(cls):
        cls.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="password",
        )

    def test_user_changelist_shows_add_button(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("admin:auth_user_changelist"))
        self.assertContains(response, reverse("admin:auth_user_add"))

    def test_group_changelist_shows_add_button(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("admin:auth_group_changelist"))
        self.assertContains(response, reverse("admin:auth_group_add"))
