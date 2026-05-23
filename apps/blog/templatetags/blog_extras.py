from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def reading_label(minutes):
    return f"{minutes} min read"


@register.simple_tag
def active_nav(request, url_name):
    from django.urls import resolve, Resolver404
    try:
        match = resolve(request.path_info)
        if match.url_name == url_name or match.view_name == url_name:
            return "active"
    except Resolver404:
        pass
    return ""


@register.filter
def truncate_words_html(value, num):
    """Truncate plain text to num words."""
    words = str(value).split()
    if len(words) <= num:
        return value
    return " ".join(words[:num]) + "…"
