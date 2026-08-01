from django.contrib import admin
from django.utils.encoding import force_str
from import_export.admin import ImportExportMixin

from .models import Event, Section
from .resources import EventResource, SectionResource


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


class EventAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = EventResource
    search_fields = (
        "name",
        "location",
    )
    list_filter = (IsArchivedListFilter,)
    list_display = (
        "name",
        "location",
        "schedule",
    )

    def get_queryset(self, request):
        return Event.all_objects.all()


@admin.register(Section)
class SectionAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = SectionResource
    search_fields = ("name",)
    list_filter = (IsArchivedListFilter,)

    def get_queryset(self, request):
        return Section.all_objects.all()


admin.site.register(Event, EventAdmin)
