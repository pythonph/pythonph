import os

import yaml
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from app.events.models import Event


class Command(BaseCommand):
    help = (
        "Populates the Event table from data/events.yaml. "
        "Safe to re-run — upserts by slug so existing records are updated "
        "rather than duplicated."
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
            slug = slugify(entry["name"])
            event, created = Event.all_objects.update_or_create(
                slug=slug,
                defaults={
                    "name": entry["name"],
                    "schedule": entry["schedule"],
                    "location": entry["location"],
                    "description": entry.get("description", ""),
                    "link": entry.get("link", ""),
                    "cover_image": "",
                    "order": entry.get("order", 0),
                    "is_removed": False,
                },
            )
            verb = "Created" if created else "Updated"
            self.stdout.write(f"  {verb} event: {event.name}")

        self.stdout.write(self.style.SUCCESS(f"Done — {Event.available_objects.count()} event(s) available."))
