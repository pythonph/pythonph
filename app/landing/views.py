from django.shortcuts import render

from app.events.models import Event
from app.landing.models import Section, SiteSettings
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

    latest_events = Event.available_objects.all()[:4]

    context = {
        "core_committees": core_committees,
        "board_of_trustees": board_of_trustees,
        "directors": directors,
        "latest_events": latest_events,
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


# ── Registration views ─────────────────────────────────────────────

from django.contrib.auth.views import LoginView  # noqa: E402
from django.shortcuts import redirect  # noqa: E402

from .forms import CustomUserCreationForm, LoginForm  # noqa: E402


def register(request):
    if not SiteSettings.load().auth_enabled:
        return redirect("landing:landing")

    if request.method == "POST":
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("landing:landing")
    else:
        form = CustomUserCreationForm()

    context = {"form": form}

    return render(request, "registration/register.html", context)


class CustomLoginView(LoginView):
    template_name = "registration/login.html"
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if not SiteSettings.load().auth_enabled:
            return redirect("landing:landing")
        return super().dispatch(request, *args, **kwargs)
