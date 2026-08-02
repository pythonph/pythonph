from django.db import models
from model_utils.models import SoftDeletableModel
from tinymce.models import HTMLField


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


class Event(SoftDeletableModel):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    cover_image = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}, {self.location} - {self.schedule}"
