from factory.django import DjangoModelFactory
from factory import PostGenerationMethodCall
from django.contrib.auth import get_user_model
from faker import Factory
from faker.providers.phone_number import Provider


class RussiaPhoneNumberProvider(Provider):
    """
    A Provider for mobile phone number.
    """

    def russian_phone_number(self):
        return f"+7{self.msisdn()}"


User = get_user_model()
faker = Factory.create()
faker.add_provider(RussiaPhoneNumberProvider)


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ("username",)

    username = faker.user_name()
    first_name = faker.first_name()
    password = PostGenerationMethodCall(
        "set_password", "12345")
    last_name = faker.last_name()
    email = faker.email()
    phone_number = faker.russian_phone_number()
    date_of_birth = faker.date_of_birth(minimum_age=18,
                                        maximum_age=45)
    closed_sales = 1
    sales_amount = 0
    photo = ""
    is_active = True
