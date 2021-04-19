from django.shortcuts import render

from .models import Event, Section


def index(request):
    events = Event.objects.all()
    sections = Section.objects.all()
    return render(request, 'landing/index.html', {
        'events': events,
        'sections': sections
    })
