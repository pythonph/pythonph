from django.db import models
from model_utils.models import SoftDeletableModel
from tinymce.models import HTMLField


class SiteSettings(models.Model):
    """Singleton model for site-wide settings editable via the Django admin."""

    show_navbar_logo = models.BooleanField(default=False)
    auth_enabled = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return "Site Settings"

    @classmethod
    def load(cls):
        """Return the singleton settings instance, creating it if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Section(SoftDeletableModel):
    slug = models.SlugField(max_length=255, unique=True)
    title = models.CharField(max_length=255, blank=True, default="")
    name = models.CharField(max_length=255)
    content = HTMLField()
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ["order"]
