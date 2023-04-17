from django.test import Client

import pytest
from unittest import mock

pytestmark = pytest.mark.django_db


def test_healthz_200_ok():
    response = Client().get("/healthz/")
    assert response.status_code == 200


def test_readiness_200_ok():
    response = Client().get("/readiness/")
    assert response.status_code == 200


def test_readiness_500_db_invalid():
    cursor = mock.MagicMock(**{"fetchone.return_value": None})
    with mock.patch("django.db.backends.utils.CursorWrapper", mock.MagicMock(side_effect=lambda x, y: cursor)):
        response = Client().get("/readiness/")
        assert response.status_code == 500
        assert response.content.decode("utf-8") == "db: invalid response"


def test_readiness_500_db_conn_err():
    with mock.patch("django.db.backends.utils.CursorWrapper", mock.MagicMock(side_effect=Exception())):
        response = Client().get("/readiness/")
        assert response.status_code == 500
        assert response.content.decode("utf-8") == "db: cannot connect to database."


def test_readiness_500_cache_conn_err():
    def mock_all(x):
        raise x

    with mock.patch(
        "django.core.cache.CacheHandler.all",
        mock.MagicMock(side_effect=lambda initialized_only: [] if initialized_only else mock_all(Exception())),
    ):
        response = Client().get("/readiness/")
        assert response.status_code == 500
        assert response.content.decode("utf-8") == "cache: cannot connect to cache."
