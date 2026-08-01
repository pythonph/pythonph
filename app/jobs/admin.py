from django.contrib import admin
from import_export.admin import ImportExportMixin
from markdownx.admin import MarkdownxModelAdmin

from .models import Company, Job
from .resources import CompanyResource, JobResource


class ImportExportMarkdownxModelAdmin(ImportExportMixin, MarkdownxModelAdmin):
    """Django admin with import/export and the markdownx form widget."""


class CompanyAdmin(ImportExportMarkdownxModelAdmin):
    resource_class = CompanyResource


class JobAdmin(ImportExportMarkdownxModelAdmin):
    resource_class = JobResource

    list_display = (
        "title",
        "company",
        "user",
        "is_active",
        "is_approved",
        "is_sponsored",
        "created_at",
        "updated_at",
    )
    search_fields = ("title",)
    list_filter = (
        "is_approved",
        "is_active",
        "is_sponsored",
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
