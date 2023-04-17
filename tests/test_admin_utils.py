import pytest

from tests.factories import DemoModelFactory
from unicef_djangolib.admin_utils import admin_reverse

pytestmark = pytest.mark.django_db


def test_admin_reverse():
    admin_url = admin_reverse(DemoModelFactory())
    assert admin_url == "/admin/sample/demomodel/"
