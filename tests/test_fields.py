from django.db import connection

import pytest

from unicef_djangolib.fields import CurrencyField, QuarterField

from demo.factories import ImageFactory
from demo.sample.models import Author, Image

pytestmark = pytest.mark.django_db


def test_currency_field():
    f = CurrencyField()
    assert f.db_parameters(connection)['type'] == 'varchar(4)'
    assert not f.db_parameters(connection)['check']


def test_quarter_field():
    f = QuarterField()
    assert f.db_parameters(connection)['type'] == 'varchar(2)'
    assert not f.db_parameters(connection)['check']


def test_coded_generic_relation(author):
    assert author.profile_image.exists() is False
    image_qs = Image.objects.filter(
        code="author_profile_image"
    )
    assert image_qs.exists() is False
    image = ImageFactory(
        name="sample.pdf",
        content_object=author,
        code="author_profile_image",
    )
    assert image_qs.exists() is True
    assert author.profile_image.first() == image

    # test filtering
    assert Author.objects.filter(
        profile_image__name="sample.pdf"
    ).exists() is True
