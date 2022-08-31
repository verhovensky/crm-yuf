import pytz
import random
from django.conf import settings
from factory import SubFactory
from datetime import timedelta
from factory.django import DjangoModelFactory, mute_signals
from django.db.models.signals import post_save
from faker import Factory
from tests.factories.users import UserProfileFactory
from tests.factories.products import ProductFactory
from order.models import Order, OrderItem


tz = pytz.timezone(settings.TIME_ZONE)
faker = Factory.create()


@mute_signals(post_save)
class OrderFactory(DjangoModelFactory):
    """ Mute post_save signal as we do not test Celery task call. """
    class Meta:
        model = Order

    full_name = faker.name()
    phone = faker.msisdn()
    address = faker.address()
    delivery_time = faker.future_datetime(tzinfo=tz) \
                    + timedelta(seconds=852)
    self_pick = random.choice([True, False])
    cash_on_delivery = random.choice([True, False])
    this_order_account = SubFactory(
        UserProfileFactory)
    this_order_client = " "
    total_sum = faker.random_int(min=1000, max=1200)
    description = faker.text()[:50]


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = SubFactory(OrderFactory)
    total = faker.random_int(min=100,
                             max=999)
    product_id = SubFactory(ProductFactory)
    name = faker.name_female()
    price = faker.random_int(min=100,
                             max=199,
                             step=8)
    quantity = faker.random_int(min=1,
                                max=20)
