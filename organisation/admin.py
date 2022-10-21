from django.contrib import admin

from .models import Commitee, Volunteer



class VolunteerAdmin(admin.ModelAdmin):
    list_display = ("display_name", "commitee", "first_name", "last_name",)
    list_filter = ("commitee",)


admin.site.register(Commitee)
admin.site.register(Volunteer, VolunteerAdmin)
