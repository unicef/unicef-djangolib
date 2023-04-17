from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission

import factory
from factory import fuzzy

from demo.sample import models


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Image


class AuthorFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")

    class Meta:
        model = models.Author


class BookFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("name")
    author = factory.SubFactory(AuthorFactory)

    class Meta:
        model = models.Book


class DemoModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.DemoModel


class DemoChildModelFactory(factory.django.DjangoModelFactory):
    parent = factory.SubFactory(DemoModelFactory)

    class Meta:
        model = models.DemoModel


class UserFactory(factory.django.DjangoModelFactory):
    username = fuzzy.FuzzyText(length=50)

    class Meta:
        model = get_user_model()


class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission
        django_get_or_create = ("codename",)
