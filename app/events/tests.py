from datetime import date

from django.test import TestCase
from django.urls import reverse

from app.events.models import Event


class EventViewsTests(TestCase):
    def setUp(self):
        self.program = Event.objects.create(
            name="PythonPH Meetups",
            slug="pythonph-meetups",
            schedule="Monthly, Every 3rd Thursday",
            location="Various locations",
            link="https://www.meetup.com/pythonph/",
            order=1,
        )
        Event.objects.create(
            name="PythonPH Meetup — September 2026",
            slug="pythonph-meetup-september-2026",
            schedule="7:00 PM",
            location="Makati",
            link="https://www.meetup.com/pythonph/events/111/",
            date=date(2026, 9, 17),
            parent=self.program,
        )
        Event.objects.create(
            name="PythonPH Meetup — October 2026",
            slug="pythonph-meetup-october-2026",
            schedule="7:00 PM",
            location="BGC",
            link="https://www.meetup.com/pythonph/events/222/",
            date=date(2026, 10, 15),
            parent=self.program,
        )
        Event.objects.create(
            name="PythonAsia 2026",
            slug="pythonasia-2026",
            schedule="March 21-23, 2026",
            location="DLSU",
            link="https://2026.pythonasia.org/",
            order=0,
        )

    def test_event_list_shows_only_programs(self):
        response = self.client.get(reverse("events:events"))
        self.assertContains(response, "PythonPH Meetups")
        self.assertContains(response, "PythonAsia 2026")
        self.assertNotContains(response, "PythonPH Meetup — September 2026")

    def test_program_detail_groups_sessions_by_month(self):
        response = self.client.get(reverse("events:event_detail", args=["pythonph-meetups"]))
        self.assertContains(response, "October 2026")
        self.assertContains(response, "September 2026")
        self.assertContains(response, "https://www.meetup.com/pythonph/events/111/")
        self.assertContains(response, "https://www.meetup.com/pythonph/events/222/")
