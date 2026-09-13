import calendar
from itertools import groupby

from django.db.models import F
from django.shortcuts import get_object_or_404, render

from app.events.models import Event


def _month_label(event):
    if event.date is None:
        return "Other"
    return f"{calendar.month_name[event.date.month]} {event.date.year}"


def event_list(request):
    programs = Event.available_objects.filter(parent__isnull=True)
    return render(request, "events/event_list.html", {"events": programs})


def event_detail(request, slug):
    event = get_object_or_404(Event.available_objects, slug=slug)
    other_events = Event.available_objects.filter(parent__isnull=True).exclude(pk=event.pk)[:3]

    children = list(event.children.filter(is_removed=False).order_by(F("date").desc(nulls_last=True), "order"))
    event_groups = [(label, list(group)) for label, group in groupby(children, key=_month_label)]

    return render(
        request,
        "events/event_detail.html",
        {
            "event": event,
            "other_events": other_events,
            "event_groups": event_groups,
        },
    )
