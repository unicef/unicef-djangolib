import pytest
from rest_framework.test import APIRequestFactory, force_authenticate
from tablib import Dataset

from demo.factories import UserFactory, DemoModelFactory
from demo.views import DemoListAPIView
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_friendly_renderer():
    user = UserFactory(is_superuser=True)
    DemoModelFactory(boolean_field=True)
    DemoModelFactory(boolean_field=False)

    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get('/sample/list/?format=csv')

    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 5
    assert dataset[0] == ('Yes', '', '1', '', '')
    assert dataset[1] == ('', '', '2', '', '')
