from import_export import resources

from .models import Event


class EventResource(resources.ModelResource):
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
            "created_at",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True
