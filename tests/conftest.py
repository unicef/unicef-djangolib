# coding=utf-8
import pytest

from tests import factories


@pytest.fixture
def author():
    return factories.AuthorFactory()


@pytest.fixture
def book():
    return factories.BookFactory()
