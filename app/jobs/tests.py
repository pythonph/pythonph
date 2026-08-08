from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Company, Job


class JobsViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="secret")
        self.approved_company = Company.objects.create(
            name="Approved Co", profile="Company profile", homepage="https://a.example.com"
        )
        self.other_company = Company.objects.create(
            name="Other Co", profile="Company profile", homepage="https://b.example.com"
        )
        self.approved_job = Job.objects.create(
            user=self.user,
            company=self.approved_company,
            title="Django Developer",
            description="**Nice** job",
            location="Makati",
            salary_range="₱80,000 - ₱120,000",
            short_description="A short blurb",
            is_remote=True,
            is_approved=True,
            is_active=True,
        )
        self.unapproved_job = Job.objects.create(
            user=self.user,
            company=self.other_company,
            title="Secret Role",
            description="pending",
            location="Manila",
            is_approved=False,
            is_active=True,
        )
        self.inactive_job = Job.objects.create(
            user=self.user,
            company=self.other_company,
            title="Old Role",
            description="inactive",
            location="Cebu",
            is_approved=True,
            is_active=False,
        )

    def test_index_shows_only_approved_active(self):
        response = self.client.get(reverse("jobs:index"))
        self.assertEqual(response.status_code, 200)
        titles = [job.title for job in response.context["page_obj"]]
        self.assertIn("Django Developer", titles)
        self.assertNotIn("Secret Role", titles)
        self.assertNotIn("Old Role", titles)

    def test_index_search_by_title(self):
        response = self.client.get(reverse("jobs:index"), {"search": "django"})
        titles = [job.title for job in response.context["page_obj"]]
        self.assertEqual(titles, ["Django Developer"])

    def test_index_search_by_company(self):
        response = self.client.get(reverse("jobs:index"), {"search": "approved"})
        titles = [job.title for job in response.context["page_obj"]]
        self.assertEqual(titles, ["Django Developer"])

    def test_index_pagination_preserves_search(self):
        for i in range(25):
            Job.objects.create(
                user=self.user,
                company=self.approved_company,
                title=f"Python Developer {i}",
                description="description",
                location="Manila",
                is_approved=True,
                is_active=True,
            )
        response = self.client.get(reverse("jobs:index"), {"search": "python", "page": 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "?page=1&search=python")

    def test_detail_renders_approved_job(self):
        response = self.client.get(reverse("jobs:job_detail", args=[self.approved_job.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Django Developer")
        self.assertContains(response, "A short blurb")
        self.assertContains(response, "application/ld+json")
        self.assertContains(response, "Approved Co")

    def test_detail_404_unapproved(self):
        response = self.client.get(reverse("jobs:job_detail", args=[self.unapproved_job.pk]))
        self.assertEqual(response.status_code, 404)

    def test_detail_404_inactive(self):
        response = self.client.get(reverse("jobs:job_detail", args=[self.inactive_job.pk]))
        self.assertEqual(response.status_code, 404)

    def test_companies_page_groups_approved_jobs(self):
        response = self.client.get(reverse("jobs:companies"))
        self.assertEqual(response.status_code, 200)
        companies = response.context["companies"]
        names = [item["company"].name for item in companies]
        self.assertIn("Approved Co", names)
        self.assertNotIn("Other Co", names)
        approved_item = next(item for item in companies if item["company"].name == "Approved Co")
        self.assertEqual(approved_item["job_count"], 1)
        self.assertEqual(len(approved_item["latest_jobs"]), 1)

    def test_post_requires_login(self):
        response = self.client.get(reverse("jobs:post"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("landing:login"), response.url)

    def test_api_returns_approved_active_with_new_fields(self):
        response = self.client.get(reverse("jobs:job-list"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("results", payload)
        self.assertEqual(payload["count"], 1)
        job = payload["results"][0]
        self.assertEqual(job["title"], "Django Developer")
        self.assertEqual(job["salary_range"], "₱80,000 - ₱120,000")
        self.assertEqual(job["short_description"], "A short blurb")
        self.assertTrue(job["is_remote"])
