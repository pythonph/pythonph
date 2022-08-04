from django.shortcuts import render

from .models import Event, Section
from organisation.models import Volunteer, Commitee


def index(request):
    events = Event.available_objects.all()
    sections = Section.available_objects.all()
    board_members = Volunteer.available_objects.filter(is_staff=True)
    commitees = Commitee.available_objects.prefetch_related('volunteers')

    return render(request, 'landing/index.html', {
        'events': events,
        'sections': sections,
        'board_members': board_members,
        'commitees': commitees,
    })
