from django.contrib.auth.models import User
from import_export import fields, resources, widgets
from taggit.models import Tag

from .models import Company, Job


class TaggitWidget(widgets.ManyToManyWidget):
    """ManyToManyWidget that creates taggit tags by name on import."""

    def clean(self, value, row=None, **kwargs):
        if not value:
            return self.model.objects.none()
        if isinstance(value, (float, int)):
            names = [str(int(value))]
        else:
            names = filter(None, [name.strip() for name in value.split(self.separator)])
        tags = [self.model.objects.get_or_create(name=name)[0] for name in names]
        return self.model.objects.filter(pk__in=[tag.pk for tag in tags])


class BaseResource(resources.ModelResource):
    """Excludes auto-managed timestamps from import (they remain exported)."""

    import_timestamps_exclude = ("created_at", "updated_at")

    def get_import_fields(self):
        return [field for field in super().get_import_fields() if field.attribute not in self.import_timestamps_exclude]


class CompanyResource(BaseResource):
    user = fields.Field(
        attribute="user",
        column_name="user",
        widget=widgets.ForeignKeyWidget(User, "username"),
    )

    class Meta:
        model = Company
        import_id_fields = ("id",)
        fields = (
            "id",
            "user",
            "name",
            "profile",
            "homepage",
            "created_at",
            "updated_at",
        )
        skip_unchanged = True
        report_skipped = True


class JobResource(BaseResource):
    user = fields.Field(
        attribute="user",
        column_name="user",
        widget=widgets.ForeignKeyWidget(User, "username"),
    )
    company = fields.Field(
        attribute="company",
        column_name="company",
        widget=widgets.ForeignKeyWidget(Company, "name"),
    )
    tags = fields.Field(
        attribute="tags",
        column_name="tags",
        widget=TaggitWidget(Tag, separator=", ", field="name"),
    )

    class Meta:
        model = Job
        import_id_fields = ("id",)
        fields = (
            "id",
            "user",
            "company",
            "is_approved",
            "is_sponsored",
            "tags",
            "title",
            "salary_range",
            "short_description",
            "description",
            "location",
            "is_remote",
            "application_url",
            "application_email",
            "created_at",
            "updated_at",
            "is_active",
        )
        skip_unchanged = True
        report_skipped = True
