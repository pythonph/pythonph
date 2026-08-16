from django.db import models
from model_utils.models import SoftDeletableModel


class Commitee(SoftDeletableModel):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Volunteer(SoftDeletableModel):
    COMMITTEE_TYPE_CHOICES = [
        ("lead", "Lead"),
        ("co_lead", "Co-Lead"),
        ("member", "Member"),
    ]

    display_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    title = models.CharField(max_length=255, blank=True, default="")
    image = models.CharField(max_length=255, blank=True, default="")
    is_staff = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    commitee = models.ForeignKey(
        Commitee,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="volunteers",
    )
    commitee_type = models.CharField(
        max_length=20,
        choices=COMMITTEE_TYPE_CHOICES,
        default="member",
    )

    def __str__(self):
        return self.display_name

    class Meta(object):
        ordering = ["order"]
