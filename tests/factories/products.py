from factory import SubFactory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from faker import Factory
from product.models import Category, Product
from tests.factories.users import UserFactory
from client.apps import slugify


User = get_user_model()
faker = Factory.create()


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = faker.name_male().replace(" ", "")
    slug = slugify(name)


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    category = SubFactory(CategoryFactory)
    name = faker.name_female().replace(" ", "")
    slug = slugify(name)
    image = ""
    price = faker.random_digit_not_null()
    stock = faker.random_digit_not_null()
    available = True
    created_by = SubFactory(UserFactory)
