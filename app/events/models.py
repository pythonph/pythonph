from django.db import models
from model_utils.models import SoftDeletableModel
from tinymce.models import HTMLField


class Event(SoftDeletableModel):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = HTMLField(blank=True, default="")
    cover_image = models.CharField(max_length=255)
    link = models.CharField(max_length=255, blank=True, default="")
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.location} - {self.schedule}"

    class Meta(object):
        ordering = ["order", "-created_at"]
