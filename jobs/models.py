from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager

from django.contrib.auth.models import User
from django.db import models


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

    def __unicode__(self):
        return self.name


class Job(models.Model):
    user = models.ForeignKey(
        User,
        related_name="companies",
        null=True,
        on_delete=models.SET_NULL,
    )
    company = models.ForeignKey(
        Company,
        null=True,
        on_delete=models.SET_NULL,
    )
    is_approved = models.BooleanField(default=False)
    is_sponsored = models.BooleanField(default=False)
    tags = TaggableManager()

    title = models.CharField(max_length=255)
    description = MarkdownxField()
    location = models.CharField(max_length=255)
    application_url = models.URLField(blank=True, null=True)
    application_email = models.EmailField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return "{} - {}".format(self.company.name, self.title)

