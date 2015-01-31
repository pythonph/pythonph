from api.models import Company, Job
from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin

admin.site.register(Company, MarkdownModelAdmin)
admin.site.register(Job, MarkdownModelAdmin)

