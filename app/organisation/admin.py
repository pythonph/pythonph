from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Commitee, Volunteer
from .resources import CommiteeResource, VolunteerResource


class CommiteeAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    resource_class = CommiteeResource
    import_form_class = ImportForm
    export_form_class = ExportForm


class VolunteerAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    resource_class = VolunteerResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = (
        "display_name",
        "commitee",
        "commitee_type",
        "first_name",
        "last_name",
    )
    list_filter = ("commitee", "commitee_type")


admin.site.register(Commitee, CommiteeAdmin)
admin.site.register(Volunteer, VolunteerAdmin)
