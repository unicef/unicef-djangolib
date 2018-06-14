from django.urls import reverse
from rest_framework.test import APIClient
from tablib import Dataset

import pytest

from demo.factories import DemoModelFactory, UserFactory


@pytest.mark.django_db
def test_export_model_view():
    user = UserFactory(is_superuser=True)
    DemoModelFactory(name='demo', boolean_field=True)
    DemoModelFactory(name='test', boolean_field=False)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('sample:list') + '?format=csv'
    response = client.get(url, format='json')

    dataset = Dataset().load(response.content.decode('utf-8'), 'csv')
    assert len(dataset._get_headers()) == 6
    assert dataset.headers == ['boolean field', 'currency', 'ID', 'Random Method', 'name', 'quarter']
