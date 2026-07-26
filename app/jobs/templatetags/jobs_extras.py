from django import template
from django.utils.safestring import mark_safe
from markdownx.utils import markdownify

register = template.Library()


@register.filter
def render_markdown(text):
    """Render a MarkdownxField value as safe HTML."""
    return mark_safe(markdownify(text or ""))
