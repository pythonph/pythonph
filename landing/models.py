from django.db import models


class Event(models.Model):
    name = models.CharField(max_length=255)
    schedule = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    cover_image = models.CharField(max_length=255)
    link = models.CharField(max_length=255)

    def __unicode__(self):
        return self.name
