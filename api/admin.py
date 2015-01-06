from api.models import Company, Job
from django.contrib import admin


class CompanyAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


class JobAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Company, CompanyAdmin)
admin.site.register(Job, JobAdmin)
