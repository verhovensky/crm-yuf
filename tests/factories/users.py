from factory import SubFactory
from factory.django import DjangoModelFactory, mute_signals
from factory import PostGenerationMethodCall
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from faker import Factory
from faker.providers.phone_number import Provider
from account.models import UserProfile


class RussiaPhoneNumberProvider(Provider):
    """
    A Provider for mobile phone number.
    """

    def russian_phone_number(self):
        return f"+7{self.msisdn()}"


User = get_user_model()
faker = Factory.create()
faker.add_provider(RussiaPhoneNumberProvider)


@mute_signals(post_save)
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
    is_active = True


@mute_signals(post_save)
class UserProfileFactory(DjangoModelFactory):
    class Meta:
        model = UserProfile
        django_get_or_create = ("user",)

    user = SubFactory(UserFactory)
    phone_number = faker.russian_phone_number()
    date_of_birth = faker.date_of_birth(minimum_age=18,
                                        maximum_age=45)
    closed_sales = 1
    sales_amount = 0
    photo = ""

