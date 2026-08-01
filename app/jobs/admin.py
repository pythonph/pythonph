from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from markdownx.models import MarkdownxField
from markdownx.widgets import AdminMarkdownxWidget
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Company, Job
from .resources import CompanyResource, JobResource


class ImportExportMarkdownxModelAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    """Unfold admin with import/export and the markdownx form widget."""

    import_form_class = ImportForm
    export_form_class = ExportForm

    formfield_overrides = {
        MarkdownxField: {"widget": AdminMarkdownxWidget},
    }


class CompanyAdmin(ImportExportMarkdownxModelAdmin):
    resource_class = CompanyResource


class JobAdmin(ImportExportMarkdownxModelAdmin):
    resource_class = JobResource

    list_display = (
        "title",
        "company",
        "location",
        "salary_range",
        "is_remote",
        "user",
        "is_active",
        "is_approved",
        "is_sponsored",
        "created_at",
        "updated_at",
    )
    search_fields = ("title", "company__name", "location")
    list_filter = (
        "is_approved",
        "is_active",
        "is_sponsored",
        "is_remote",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
