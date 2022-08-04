from model_utils.models import SoftDeletableModel

from django.db import models


class Commitee(SoftDeletableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Volunteer(SoftDeletableModel):
    display_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    title = models.CharField(max_length=255, blank=True, default='')
    is_staff = models.BooleanField(default=False)
    commitee = models.ForeignKey(
        Commitee,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='volunteers',
    )

    def __str__(self):
        return self.display_name
