from django.contrib import admin
from import_export.admin import ImportExportMixin, ImportExportModelAdmin

from .models import Commitee, Volunteer
from .resources import CommiteeResource, VolunteerResource


class CommiteeAdmin(ImportExportModelAdmin):
    resource_class = CommiteeResource


class VolunteerAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = VolunteerResource
    list_display = (
        "display_name",
        "commitee",
        "first_name",
        "last_name",
    )
    list_filter = ("commitee",)


admin.site.register(Commitee, CommiteeAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
