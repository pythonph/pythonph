from api.v1 import api
from django.shortcuts import render


def index(request):
    context = dict(
        api_version=api.api_name,
    )
    return render(request, 'index.html', context)
