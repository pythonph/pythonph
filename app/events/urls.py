from django.urls import path

from .views import event_detail, event_list

app_name = "events"

urlpatterns = (
    path("", event_list, name="events"),
    path("<slug:slug>/", event_detail, name="event_detail"),
)
