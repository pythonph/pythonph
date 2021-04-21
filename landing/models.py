from ckeditor.fields import RichTextField
from django.db import models
from model_utils.models import SoftDeletableModel


class Section(SoftDeletableModel):
    name = models.CharField(max_length=255)
    content = RichTextField()
    order = models.PositiveIntegerField(default=0)

    def __unicode(self):
        return self.name

    def __str__(self):
        return self.name

    class Meta(object):
        ordering = ['order']


class Event(SoftDeletableModel):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    cover_image = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name

    def __str__(self):
        return f'{self.name}, {self.location} - {self.schedule}'
