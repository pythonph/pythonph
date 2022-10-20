from django.shortcuts import render

from .models import Event, Section
from organisation.models import Volunteer, Commitee


def index(request):
    events = Event.available_objects.all()
    sections = Section.available_objects.all()
    board_members = Volunteer.available_objects.filter(is_staff=True)
    commitees = Commitee.available_objects.prefetch_related('volunteers')
    python_hour = [
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "Let's create animated Memes using Python and MoviePy",
            "date": "Thursday, October 13, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_1.png"
        },
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "API Development using Flask",
            "date": "Thursday, October 20, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_2.png"
        },
        {
            "link": "#",
            "tag": "Python Hour",
            "title": "Data Science using Python!",
            "date": "Thursday, October 27, 2022",
            "time": "7PM-8PM PHT",
            "location": "Via Zoom and Youtube Live",
            "cover_image": "landing/assets/img/python_hour/python_hour_3.png"
        }
    ]

    return render(request, 'landing/index.html', {
        'events': events,
        'sections': sections,
        'board_members': board_members,
        'commitees': commitees,
        'python_hour': python_hour,
    })
