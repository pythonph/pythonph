from django.conf.urls import patterns, url

urlpatterns = patterns(
    'jobs.views',
    url(r'^$', 'index', name='index'),
)

