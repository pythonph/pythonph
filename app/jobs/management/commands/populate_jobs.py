import random

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from faker import Faker

from app.jobs.models import Company, Job

TECH_ROLES = [
    "Python Developer",
    "Django Developer",
    "FastAPI Developer",
    "Data Engineer",
    "Machine Learning Engineer",
    "Backend Engineer",
    "Full Stack Developer",
    "DevOps Engineer",
    "Site Reliability Engineer",
    "Software Architect",
]

PH_CITIES = [
    "Manila",
    "Makati",
    "BGC",
    "Ortigas",
    "Quezon City",
    "Cebu City",
    "Davao City",
    "Pasig",
    "Mandaluyong",
    "Pasay",
]


class Command(BaseCommand):
    help = "Populates the jobs table with sample data using Faker."

    def add_arguments(self, parser):
        parser.add_argument("--count", type=int, default=20, help="Number of jobs to create")
        parser.add_argument("--companies", type=int, default=10, help="Number of companies to create")

    def handle(self, *args, **kwargs):
        fake = Faker()
        count = kwargs["count"]

        # Rebuild the sample dataset from scratch.
        Job.objects.all().delete()
        Company.objects.all().delete()

        # Jobs require a user (non-null FK) — reuse a staff user or create a demo one.
        user = User.objects.filter(is_staff=True).first()
        if user is None:
            user, _ = User.objects.get_or_create(
                username="demo",
                defaults={"email": "demo@example.com", "is_staff": True},
            )

        companies = []
        for _ in range(kwargs["companies"]):
            company = Company.objects.create(
                user=user,
                name=fake.unique.company(),
                profile="\n".join([fake.paragraph() for _ in range(3)]),
                homepage=fake.url(),
            )
            companies.append(company)

        for _ in range(count):
            min_salary = random.randint(40, 200)
            max_salary = min_salary + random.randint(20, 100)
            seniority = random.choice(["Junior", "Mid-Level", "Senior", "Lead"])
            title = f"{seniority} {random.choice(TECH_ROLES)}"
            company = random.choice(companies)

            job = Job.objects.create(
                user=user,
                company=company,
                is_approved=True,
                is_active=True,
                is_remote=random.choice([True, False, True]),
                title=title,
                salary_range=f"₱{min_salary * 1000:,} - ₱{max_salary * 1000:,}",
                short_description=fake.sentence(nb_words=15)[:100],
                description="\n".join(
                    [
                        fake.paragraph(),
                        "\nKey Responsibilities:\n",
                        *[f"• {fake.sentence()}" for _ in range(4)],
                        "\nRequirements:\n",
                        *[f"• {fake.sentence()}" for _ in range(4)],
                    ]
                ),
                location=random.choice(PH_CITIES),
                application_url=fake.url(),
                application_email=fake.email(),
            )
            job.tags.set(random.sample(TECH_ROLES, k=random.randint(1, 3)))

            self.stdout.write(self.style.SUCCESS(f"Created job: {job.title} at {company.name}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully created {count} jobs across {len(companies)} companies"))
