from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify
from taggit.managers import TaggableManager


class Company(models.Model):
    class Meta:
        verbose_name_plural = "companies"

    user = models.ForeignKey(User)

    name = models.CharField(max_length=255)
    slug = models.SlugField()
    profile = models.TextField()
    homepage = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:50].rstrip("-")
        return super(Company, self).save(*args, **kwargs)


class Job(models.Model):
    user = models.ForeignKey(User)
    company = models.ForeignKey(Company)
    tags = TaggableManager()

    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    location = models.CharField(max_length=255)
    application_url = models.URLField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:50].rstrip("-")
        return super(Job, self).save(*args, **kwargs)
