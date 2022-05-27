from django.conf import settings
from django.template import Context, Template
from django.test import override_settings


@override_settings(
    VERSION='2.2',
    FOOTER_LOGO='/static/images/UNICEF_logo_white.png'
)
def test_djangolib_allowed_settings():
    context = Context({})
    template_to_render = Template(
        '{% load djangolib %}'
        '{% html_settings "NAME" %}'
        '{% html_settings "VERSION" %}'
        '{% html_settings "BACKGROUND_COLOR" %}'
        '{% html_settings "HEADER_RIGHT_LOGO" %}'
        '{% html_settings "HEADER_LEFT_LOGO" %}'
        '{% html_settings "HOME_URL_NAME" %}'
        '{% html_settings "FOOTER_LOGO" %}'
    )
    rendered = template_to_render.render(context)
    for setting in ['NAME', 'VERSION', 'BACKGROUND_COLOR', 'HOME_URL_NAME', 'FOOTER_LOGO']:
        assert getattr(settings, setting) in rendered


def test_djangolib_not_allowed_setting():
    context = Context({})
    template_to_render = Template(
        '{% load djangolib %}'
        '{% html_settings "LANGUAGE_CODE" %}'
    )
    rendered = template_to_render.render(context)
    assert settings.LANGUAGE_CODE not in rendered
