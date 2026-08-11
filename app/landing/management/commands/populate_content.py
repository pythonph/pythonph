import os

import yaml
from django.core.management.base import BaseCommand

from app.landing.models import Section
from app.organisation.models import Commitee, Volunteer


class Command(BaseCommand):
    help = (
        "Populates landing page sections and team members from YAML files "
        "in the data/ directory. Safe to re-run — updates existing records "
        "by slug (sections) or display_name+committee (volunteers)."
    )

    def handle(self, *args, **kwargs):
        base_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "data")

        # ── Sections ──────────────────────────────────────────────────
        sections_path = os.path.join(base_dir, "sections.yaml")
        if os.path.exists(sections_path):
            with open(sections_path) as fh:
                sections_data = yaml.safe_load(fh)

            for entry in sections_data:
                section, created = Section.objects.update_or_create(
                    slug=entry["slug"],
                    defaults={
                        "title": entry.get("title", ""),
                        "name": entry["name"],
                        "content": entry["content"],
                        "order": entry.get("order", 0),
                    },
                )
                verb = "Created" if created else "Updated"
                self.stdout.write(f"  {verb} section: {section.slug}")
        else:
            self.stdout.write(self.style.WARNING(f"Skipping sections — {sections_path} not found"))

        # ── Volunteers ────────────────────────────────────────────────
        volunteers_path = os.path.join(base_dir, "volunteers.yaml")
        if os.path.exists(volunteers_path):
            with open(volunteers_path) as fh:
                volunteers_data = yaml.safe_load(fh)

            for committee_name, members in volunteers_data.items():
                committee, _ = Commitee.objects.get_or_create(name=committee_name)

                for entry in members:
                    volunteer, created = Volunteer.objects.get_or_create(
                        display_name=entry["display_name"],
                        commitee=committee,
                        defaults={
                            "first_name": entry.get("first_name", ""),
                            "last_name": entry.get("last_name", ""),
                            "title": entry.get("title", ""),
                            "image": entry.get("image", ""),
                            "order": entry.get("order", 0),
                        },
                    )
                    if not created:
                        volunteer.first_name = entry.get("first_name", "")
                        volunteer.last_name = entry.get("last_name", "")
                        volunteer.title = entry.get("title", "")
                        volunteer.image = entry.get("image", "")
                        volunteer.order = entry.get("order", 0)
                        volunteer.save()
                    verb = "Created" if created else "Updated"
                    self.stdout.write(f"  {verb} volunteer: {volunteer.display_name} ({committee.name})")
        else:
            self.stdout.write(self.style.WARNING(f"Skipping volunteers — {volunteers_path} not found"))

        self.stdout.write(self.style.SUCCESS("Done."))
