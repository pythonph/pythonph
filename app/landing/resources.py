from import_export import resources

from .models import Section


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
