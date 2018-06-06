import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from demo.factories import UserFactory


@pytest.mark.django_db
def test_is_super_user():

    user = UserFactory(is_superuser=True)

    client = APIClient()

    list_url = reverse('sample:list')
    response = client.get(list_url)
    assert response.status_code == 403

    client.force_authenticate(user=user)
    response = client.get(list_url)
    assert response.status_code == 200
