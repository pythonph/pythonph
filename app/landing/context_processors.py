from .models import SiteSettings


def site_settings(request):
    """Expose the singleton SiteSettings instance to all templates."""
    return {"site_settings": SiteSettings.load()}
