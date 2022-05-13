from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def html_settings(name):
    _settings = (
        "NAME", "VERSION", "BACKGROUND_COLOR",
        "HEADER_RIGHT_LOGO", "HEADER_LEFT_LOGO", "FOOTER_LOGO",
        "HOME_URL_NAME"
    )
    if name in _settings:
        return mark_safe(getattr(settings, name, ''))
    return ''
