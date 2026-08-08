from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.landing.urls", namespace="landing")),
    path("events/", include("app.events.urls", namespace="events")),
    path("jobs/", include("app.jobs.urls", namespace="jobs")),
    path("markdownx/", include("markdownx.urls")),
    path("tinymce/", include("tinymce.urls")),
]

urlpatterns.append(path("__reload__/", include("django_browser_reload.urls")))

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.insert(0, path("__debug__/", include(debug_toolbar.urls)))

if settings.APP_ENV == "development":
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
