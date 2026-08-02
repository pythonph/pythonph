from django.shortcuts import render

from app.landing.models import Section
from app.organisation.models import Commitee, Volunteer


def index(request):
    board_of_trustees = Volunteer.available_objects.filter(
        commitee__name="Board of Trustees",
    ).order_by("order")

    directors = Volunteer.available_objects.filter(
        commitee__name="Directors",
    ).order_by("order")

    core_committees = Commitee.available_objects.exclude(name__in=["Board of Trustees", "Directors"]).prefetch_related(
        "volunteers"
    )

    context = {
        "core_committees": core_committees,
        "board_of_trustees": board_of_trustees,
        "directors": directors,
    }

    # Add each landing-page section as a named context variable so
    # templates can render {{ our_aim.content|safe }} etc.
    section_slugs = [
        "header_intro",
        "our_aim",
        "why_python",
        "what_we_do_intro",
        "code_of_conduct",
        "mailing_list",
    ]
    for slug in section_slugs:
        try:
            context[slug] = Section.available_objects.get(slug=slug)
        except Section.DoesNotExist:
            pass

    return render(request, "landing/index.html", context)
