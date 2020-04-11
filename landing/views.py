from django.shortcuts import render

from .models import Event


def index(request):
    events = Event.objects.all()
    return render(request, 'landing/index.html', {'events': events})
