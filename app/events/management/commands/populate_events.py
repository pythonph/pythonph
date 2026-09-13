import os
from datetime import date

import yaml
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from app.events.models import Event


def _parse_date(value):
    if isinstance(value, date):
        return value
    return date.fromisoformat(value)


class Command(BaseCommand):
    help = (
        "Populates the Event table from data/events.yaml. "
        "Safe to re-run — upserts by slug so existing records are updated "
        "rather than duplicated. Top-level entries are programs; nested "
        "'events' entries are individual sessions under that program."
    )

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data")
        events_path = os.path.join(base_dir, "events.yaml")

        if not os.path.exists(events_path):
            self.stdout.write(self.style.WARNING(f"Skipping events — {events_path} not found"))
            return

        with open(events_path) as fh:
            events_data = yaml.safe_load(fh)

        for entry in events_data:
            program, created = Event.all_objects.update_or_create(
                slug=slugify(entry["name"]),
                defaults={
                    "name": entry["name"],
                    "schedule": entry["schedule"],
                    "location": entry["location"],
                    "description": entry.get("description", ""),
                    "link": entry.get("link", ""),
                    "cover_image": "",
                    "order": entry.get("order", 0),
                    "parent": None,
                    "date": None,
                    "is_removed": False,
                },
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} program: {program.name}")

            for session in entry.get("events", []):
                session_obj, s_created = Event.all_objects.update_or_create(
                    slug=slugify(session["name"]),
                    defaults={
                        "name": session["name"],
                        "schedule": session.get("schedule", ""),
                        "location": session.get("location", ""),
                        "description": session.get("description", ""),
                        "link": session.get("link", ""),
                        "cover_image": "",
                        "order": session.get("order", 0),
                        "parent": program,
                        "date": _parse_date(session["date"]),
                        "is_removed": False,
                    },
                )
                sverb = "Created" if s_created else "Updated"
                self.stdout.write(f"    {sverb} session: {session_obj.name}")

        self.stdout.write(self.style.SUCCESS(f"Done — {Event.available_objects.count()} event(s) available."))
