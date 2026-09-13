from import_export import fields, resources, widgets

from .models import Event


class EventResource(resources.ModelResource):
    parent = fields.Field(
        column_name="parent",
        attribute="parent",
        widget=widgets.ForeignKeyWidget(Event, field="slug"),
    )

    class Meta:
        model = Event
        import_id_fields = ("id",)
        fields = (
            "id",
            "name",
            "slug",
            "schedule",
            "location",
            "description",
            "cover_image",
            "link",
            "date",
            "parent",
            "created_at",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True
