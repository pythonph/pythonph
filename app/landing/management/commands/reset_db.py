import os

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection, connections


class Command(BaseCommand):
    help = "Drops the entire database. Works with SQLite and PostgreSQL."

    def handle(self, *args, **kwargs):
        vendor = connection.vendor

        if vendor == "sqlite":
            db_path = settings.DATABASES["default"]["NAME"]
            connections.close_all()
            if os.path.exists(db_path):
                os.remove(db_path)
                self.stdout.write(f"  Deleted: {db_path}")
            else:
                self.stdout.write(f"  Not found: {db_path}")
            self.stdout.write(self.style.SUCCESS("SQLite database deleted."))

        elif vendor == "postgresql":
            with connection.cursor() as cursor:
                cursor.execute(
                    "DO $$ DECLARE r RECORD; BEGIN "
                    "FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP "
                    "EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE'; "
                    "END LOOP; END $$;"
                )
            self.stdout.write(self.style.SUCCESS("All PostgreSQL tables dropped."))

        else:
            self.stdout.write(self.style.ERROR(f"Unsupported database vendor: {vendor}"))
