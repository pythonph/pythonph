from django.contrib import admin
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from tinymce.models import HTMLField
from tinymce.widgets import AdminTinyMCE
from unfold.admin import ModelAdmin as UnfoldModelAdmin
from unfold.admin import TabularInline as UnfoldTabularInline
from unfold.contrib.filters.admin import DropdownFilter as UnfoldDropdownFilter
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from .models import Event
from .resources import EventResource

TOP_LEVEL_VALUE = "top-level"


class IsArchivedListFilter(admin.SimpleListFilter):
    title = "Archived?"
    parameter_name = "is_removed"

    def lookups(self, request, model_admin):
        return ((True, "Yes"),)

    def choices(self, changelist):
        yield {
            "selected": self.value() is None,
            "query_string": changelist.get_query_string({}, [self.parameter_name]),
            "display": "No",
        }
        for lookup, title in self.lookup_choices:
            yield {
                "selected": self.value() == force_str(lookup),
                "query_string": changelist.get_query_string({self.parameter_name: lookup}, []),
                "display": title,
            }

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(is_removed=True)
        return queryset.filter(is_removed=False)


class ParentEventFilter(UnfoldDropdownFilter):
    """Filter the changelist by parent event.

    Only events that actually have children are listed, plus a top-level option
    for the common case of events without a parent. Archived events are left out
    on both sides so the choices match the "Archived? = No" default.
    """

    title = "Parent event"
    parameter_name = "parent"

    def lookups(self, request, model_admin):
        parents = Event.all_objects.filter(is_removed=False, children__is_removed=False).order_by("name").distinct()
        return [
            (TOP_LEVEL_VALUE, "Top-level events (no parent)"),
            *[(str(parent.pk), parent.name) for parent in parents],
        ]

    def queryset(self, request, queryset):
        value = self.value()
        if value == TOP_LEVEL_VALUE:
            return queryset.filter(parent__isnull=True)
        if value:
            return queryset.filter(parent_id=value)
        return queryset


class ChildEventInline(UnfoldTabularInline):
    """Read-only section listing the event's child events.

    Children are managed from their own change page (``parent`` field), so the
    inline is intentionally display-only: no add, no delete, no editing.
    """

    model = Event
    fk_name = "parent"
    verbose_name = "Child event"
    verbose_name_plural = "Child events"
    fields = ("child_event", "schedule", "location", "date", "order")
    readonly_fields = fields
    extra = 0
    max_num = 0
    can_delete = False
    hide_title = True

    @admin.display(description="Event")
    def child_event(self, obj):
        url = reverse("admin:events_event_change", args=(obj.pk,))
        return format_html('<a href="{}">{}</a>', url, obj.name)


@admin.register(Event)
class EventAdmin(UnfoldModelAdmin, ImportExportModelAdmin):
    resource_class = EventResource
    import_form_class = ImportForm
    export_form_class = ExportForm
    formfield_overrides = {HTMLField: {"widget": AdminTinyMCE}}
    prepopulated_fields = {"slug": ("name",)}
    search_fields = (
        "name",
        "location",
        "slug",
    )
    list_filter = (IsArchivedListFilter, ParentEventFilter)
    # Unfold only wraps the filter panel in a GET form when this is set, and the
    # dropdown filters (e.g. Parent event) need it to submit.
    list_filter_submit = True
    list_display = (
        "name",
        "location",
        "schedule",
        "date",
        "parent",
        "order",
        "created_at",
    )
    list_editable = ("order",)
    autocomplete_fields = ("parent",)
    inlines = (ChildEventInline,)

    def get_queryset(self, request):
        return Event.all_objects.all()

    def get_inline_instances(self, request, obj=None):
        # Only show the section for events that actually have child events, so
        # leaf events do not get an empty table on their detail page.
        if obj is None or not obj.children.exists():
            return []
        return super().get_inline_instances(request, obj)
