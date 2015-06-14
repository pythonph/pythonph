from django.conf.urls import patterns, url

urlpatterns = patterns(
    'landing.views',
    url(r'^$', 'index', name='landing'),
)

