from django.conf.urls import patterns, url

urlpatterns = patterns(
    'jobs.views',
    url(r'^$', 'index', name='jobs'),
    url(r'^post$', 'post', name='jobs_post'),
)

