from django.contrib import admin
from django.utils.encoding import force_str
from import_export.admin import ImportExportModelAdmin
from tinymce.models import HTMLField
from tinymce.widgets import AdminTinyMCE
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Section, SiteSettings
from .resources import SectionResource


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


@admin.register(Section)
class SectionAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    resource_class = SectionResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {HTMLField: {"widget": AdminTinyMCE}}
    search_fields = ("name",)
    list_filter = (IsArchivedListFilter,)

    def get_queryset(self, request):
        return Section.all_objects.all()


@admin.register(SiteSettings)
class SiteSettingsAdmin(UnfoldModelAdmin):
    """Keep a single editable SiteSettings row."""

    def has_add_permission(self, request):
        # Only allow one singleton instance.
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
