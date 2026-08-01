from django.contrib.auth.models import User
from django.db import models
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    user = models.ForeignKey(
        User,
        related_name="companies",
        null=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(max_length=255)
    profile = MarkdownxField()
    homepage = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(
        User,
        related_name="jobs",
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="jobs",
    )
    is_approved = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    tags = TaggableManager()

    title = models.CharField(max_length=255)
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    short_description = models.CharField(max_length=100, blank=True, null=True)
    description = MarkdownxField()
    location = models.CharField(max_length=255)
    is_remote = models.BooleanField(default=False)
    application_url = models.URLField(blank=True, null=True)
    application_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} at {self.company.name}"
