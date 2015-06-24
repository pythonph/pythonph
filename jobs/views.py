from django.shortcuts import render


def index(request):
    context = dict(api_version='v1')
    return render(request, 'jobs/index.html', context)


def post(request):
    return render(request, 'jobs/post.html')
