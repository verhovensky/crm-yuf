import factory
from factory.django import DjangoModelFactory
from faker import Factory
from tests.factories.users import UserFactory
from client.models import Client, CLIENTTYPE, ORIGINS
from django.template.defaultfilters import slugify as django_slugify

faker = Factory.create()


class ClientFactory(DjangoModelFactory):

    class Meta:
        model = Client
        django_get_or_create = ("phone_number",)

    name = factory.Sequence(
        lambda x: faker.name_male())
    slug = django_slugify(name)
    phone_number = factory.Sequence(
        lambda n: "7926784%04d" % n)
    email = factory.Sequence(
        lambda e: faker.company_email())
    type = faker.random_choices(
        elements=CLIENTTYPE, length=1)[0][0]
    origin = faker.random_choices(
        elements=ORIGINS, length=1)[0][0]
    created_by = factory.SubFactory(
        UserFactory)
