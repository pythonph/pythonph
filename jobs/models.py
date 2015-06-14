from django.contrib.auth.models import User
from django.db import models
from django_markdown.models import MarkdownField
from taggit.managers import TaggableManager


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    user = models.ForeignKey(User)

    name = models.CharField(max_length=255)
    profile = MarkdownField()
    homepage = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    tags = TaggableManager()

    title = models.CharField(max_length=255)
    description = MarkdownField()
    location = models.CharField(max_length=255)
    application_url = models.URLField(blank=True, null=True)
    application_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

