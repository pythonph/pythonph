from import_export import resources

from .models import Event, Section


class EventResource(resources.ModelResource):
    class Meta:
        model = Event
        import_id_fields = ("id",)
        fields = (
            "id",
            "name",
            "schedule",
            "location",
            "cover_image",
            "link",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True


class SectionResource(resources.ModelResource):
    class Meta:
        model = Section
        import_id_fields = ("id",)
        fields = (
            "id",
            "name",
            "content",
            "order",
            "is_removed",
        )
        skip_unchanged = True
        report_skipped = True
