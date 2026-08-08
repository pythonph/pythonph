from django.contrib import admin
from django.utils.encoding import force_str
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Event
from .resources import EventResource


class IsArchivedListFilter(admin.SimpleListFilter):
    title = "Archived?"
    parameter_name = "is_removed"

    def lookups(self, request, model_admin):
        return ((True, "Yes"),)

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, [self.parameter_name]),
            "display": "No",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == force_str(lookup),
                "query_string": changelist.get_query_string({self.parameter_name: lookup}, []),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(is_removed=True)
        return queryset.filter(is_removed=False)


@admin.register(Event)
class EventAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    resource_class = EventResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    prepopulated_fields = {"slug": ("name",)}
    search_fields = (
        "name",
        "location",
        "slug",
    )
    list_filter = (IsArchivedListFilter,)
    list_display = (
        "name",
        "location",
        "schedule",
        "order",
        "created_at",
    )
    list_editable = ("order",)

    def get_queryset(self, request):
        return Event.all_objects.all()
