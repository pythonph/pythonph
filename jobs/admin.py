from django.contrib import admin
from django_markdown.admin import MarkdownModelAdmin
from jobs.models import Company, Job

admin.site.register(Company, MarkdownModelAdmin)
admin.site.register(Job, MarkdownModelAdmin)

