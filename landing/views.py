from django.shortcuts import render

from .models import Event, Section
from organisation.models import Volunteer


def index(request):
    events = Event.objects.all()
    sections = Section.objects.all()
    board_members = Volunteer.objects.filter(is_staff=True)
    return render(request, 'landing/index.html', {
        'events': events,
        'sections': sections,
        'board_members': board_members,
    })
