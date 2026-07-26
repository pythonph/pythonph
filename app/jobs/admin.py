from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Company, Job


class JobAdmin(MarkdownxModelAdmin):
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


admin.site.register(Company, MarkdownxModelAdmin)
admin.site.register(Job, JobAdmin)
