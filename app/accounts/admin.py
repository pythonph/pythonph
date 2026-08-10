"""Auth admin registrations.

Django's stock ``UserAdmin``/``GroupAdmin`` subclass the plain admin
``ModelAdmin``, which lacks unfold's ``show_add_link`` attribute. Unfold's
changelist template hides the add button for such admins, so the Users and
Groups pages render without one. Mixing in ``unfold.admin.ModelAdmin`` restores
the button (and the unfold look) without changing auth behaviour.
"""

from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, User
from unfold.admin import ModelAdmin as UnfoldModelAdmin

admin.site.unregister(Group)
admin.site.unregister(User)


@admin.register(User)
class UserAdmin(BaseUserAdmin, UnfoldModelAdmin):
    pass


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, UnfoldModelAdmin):
    pass
