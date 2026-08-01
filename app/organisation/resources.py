from import_export import fields, resources, widgets

from .models import Commitee, Volunteer


class CommiteeResource(resources.ModelResource):
    class Meta:
        model = Commitee
        import_id_fields = ("id",)
        fields = (
            "id",
            "name",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True


class VolunteerResource(resources.ModelResource):
    commitee = fields.Field(
        attribute="commitee",
        column_name="commitee",
        widget=widgets.ForeignKeyWidget(Commitee, "name"),
    )

    class Meta:
        model = Volunteer
        import_id_fields = ("id",)
        fields = (
            "id",
            "display_name",
            "first_name",
            "last_name",
            "title",
            "is_staff",
            "commitee",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True
