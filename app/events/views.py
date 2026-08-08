from django.shortcuts import get_object_or_404, render

from app.events.models import Event


def event_list(request):
    events = Event.available_objects.all()
    return render(request, "events/event_list.html", {"events": events})


def event_detail(request, slug):
    event = get_object_or_404(Event.available_objects, slug=slug)
    other_events = Event.available_objects.exclude(pk=event.pk)[:3]
    return render(
        request,
        "events/event_detail.html",
        {"event": event, "other_events": other_events},
    )
