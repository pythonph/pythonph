from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin

from .models import Company, Job


admin.site.register(Company, MarkdownxModelAdmin)
admin.site.register(Job, MarkdownxModelAdmin)
