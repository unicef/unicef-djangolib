from django.urls import reverse
from rest_framework.test import APIClient

import pytest

from demo.factories import DemoModelFactory, UserFactory


@pytest.mark.django_db
@pytest.mark.parametrize("query_string, results_len ", [('', 2), ('?name=demo', 1), ('?search=de', 1)])
def test_query_string_api_view(query_string, results_len):
    user = UserFactory(is_superuser=True)
    DemoModelFactory(name='demo', boolean_field=True)
    DemoModelFactory(name='test', boolean_field=False)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('sample:list') + query_string
    results = client.get(url, format='json').json()

    assert len(results) == results_len
