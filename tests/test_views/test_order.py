from unittest.mock import Mock, patch
from datetime import datetime, timedelta
from pytz import timezone
from django.contrib.auth.models import Group
from django.core.management import call_command
from tests.factories.users import UserProfileFactory, UserFactory
from tests.factories.clients import ClientFactory
from tests.factories.products import ProductFactory
from tests.factories.orders import OrderFactory
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings

tz = timezone(settings.TIME_ZONE)
delivery_time = datetime.now(tz=tz) + timedelta(days=1)

data = {"status": 2,
        "full_name": "some name",
        "address": "Some street 10",
        "phone": "79287656457",
        "delivery_time": delivery_time,
        "description": "Just random string"}


def setUpModule():
    call_command("create_groups")


class OrderCreateViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command("clear_cache")
        cls.user = UserFactory.create()
        cls.my_user = UserProfileFactory.create(user=cls.user)
        cls.order_client = ClientFactory.create()
        cls.product = ProductFactory.create()
        cls.create_url = reverse("order:create")
        cls.client = Client()
        cls.order_form_data = data
        cls.cart = {"1": {"quantity": "1.00",
                          "price": "111.0",
                          "product": cls.product.id,
                          "total_price": "111.00"}}

    # TODO: single self.order_form_data dict for all tests

    def setUp(self) -> None:
        group_sellers = Group.objects.get(name="Sellers")
        self.user.groups.add(group_sellers)
        self.order_form_data.update({
            "this_order_client": self.order_client.id})
        self.client.login(username=self.user,
                          password="12345")
        self.session = self.client.session
        self.session["cart"] = self.cart
        self.session.save()

    def test_create_no_group(self):
        self.user.groups.clear()
        response = self.client.post(
            self.create_url,
            data=self.order_form_data)
        self.assertEqual(response.status_code, 403)

    def test_create_cart_empty(self):
        self.session["cart"] = {}
        self.session.save()
        response = self.client.post(
            self.create_url,
            data=self.order_form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response,
                            "Недостаточно товара!")

    @patch("order.tasks.expire_order")
    def test_create_for_client(self, expire_order):
        expire_order.apply_async = Mock(return_value=True)
        response = self.client.post(
            self.create_url,
            data=self.order_form_data,
            follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context_data["object"].this_order_client,
            self.order_client)
        self.assertEqual(
            response.context_data["object"].description,
            self.order_form_data["description"])
        expire_order.apply_async.\
            assert_called_once_with(
                kwargs={"order_id":
                        response.context_data["object"].pk},
                eta=self.order_form_data["delivery_time"].
                        astimezone(),
                queue="order",
                serializer="json")

    @patch("order.tasks.expire_order")
    def test_create_new_client(self, expire_order):
        expire_order.apply_async = Mock(return_value=True)
        self.order_form_data.pop("this_order_client")
        self.order_form_data.update({"new_client": True})
        response = self.client.post(self.create_url,
                                    data=self.order_form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object"].address,
                         self.order_form_data["address"])
        self.assertEqual(response.context_data["object"]
                         .this_order_client.name,
                         self.order_form_data["full_name"])
        self.assertEqual(response.context_data["object"]
                         .this_order_client.phone_number,
                         self.order_form_data["phone"])
        self.assertNotEqual(len(response.context_data["object"]
                                .this_order_client.slug), 0)
        expire_order.apply_async.\
            assert_called_once_with(
                kwargs={"order_id":
                        response.context_data["object"].pk},
                eta=self.order_form_data["delivery_time"].
                        astimezone(),
                queue="order",
                serializer="json")

    @patch("order.tasks.expire_order")
    def test_create_for_other(self, expire_order):
        expire_order.apply_async = Mock(return_value=True)
        self.order_form_data.update({"for_other": True})
        response = self.client.post(self.create_url,
                                    data=self.order_form_data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context_data["object"].this_order_client,
                         self.order_client)
        self.assertEqual(response.context_data["object"].full_name,
                         self.order_form_data["full_name"])
        self.assertEqual(response.context_data["object"].phone,
                         self.order_form_data["phone"])
        self.assertEqual(response.context_data["object"].address,
                         self.order_form_data["address"])
        expire_order.apply_async.\
            assert_called_once_with(
                kwargs={"order_id":
                        response.context_data["object"].pk},
                eta=self.order_form_data["delivery_time"].
                        astimezone(),
                queue="order",
                serializer="json")


class OrderChanageViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        call_command("clear_cache")
        cls.user = UserFactory.create()
        cls.my_user = UserProfileFactory.create(
            user=cls.user)
        cls.order_client = ClientFactory.create()
        cls.data = data
        cls.my_order = OrderFactory.create(
            this_order_client=cls.order_client,
            updated_by=cls.my_user)
        cls.change_url = reverse("order:change",
                                 kwargs={"pk": cls.my_order.pk})

    def setUp(self) -> None:
        self.client = Client()
        self.client.login(username=self.user,
                          password="12345")

    def test_sellers_can_not_change(self):
        group_sellers = Group.objects.get(name="Sellers")
        self.user.groups.add(group_sellers)
        response = self.client.post(self.change_url,
                                    data=self.data)
        self.assertEqual(response.status_code, 403)

    def test_managers_change(self):
        group_managers = Group.objects.get(name="Managers")
        self.user.groups.add(group_managers)
        response = self.client.post(self.change_url,
                                    data=self.data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        # Refresh from DB so we got updated version of our objects
        self.my_order.refresh_from_db()
        self.my_user.refresh_from_db()
        self.assertEqual(self.my_order.description,
                         self.data["description"])
        self.assertEqual(self.my_order.status,
                         self.data["status"])
        self.assertEqual(self.my_order.full_name,
                         self.data["full_name"])
        self.assertEqual(self.my_order.address,
                         self.data["address"])
        self.assertEqual(self.my_order.phone,
                         self.data["phone"])
        self.assertEqual(self.my_user.closed_sales, 2)
        self.assertEqual(self.my_user.sales_amount,
                         self.my_order.total_sum)

    def test_decreases_on_bad_status_change(self):
        group_managers = Group.objects.get(name="Managers")
        self.user.groups.add(group_managers)
        for i in range(3, 6):
            self.my_order.status = 2
            self.my_user.sales_amount = \
                self.my_order.total_sum
            self.my_user.closed_sales = 2
            self.my_user.save()
            self.my_order.save()
            self.client.post(self.change_url,
                             data={"status": i},
                             follow=True)
            self.my_user.refresh_from_db()
            self.assertEqual(self.my_user.sales_amount, 0)
            self.assertEqual(self.my_user.closed_sales, 1)

    def test_not_decreases_on_bad_statuses_change(self):
        group_managers = Group.objects.get(name="Managers")
        self.user.groups.add(group_managers)
        self.my_user.sales_amount = self.my_order.total_sum
        self.my_user.closed_sales = 2
        self.my_user.save()
        for i in range(3, 6):
            self.client.post(self.change_url,
                             data={"status": i},
                             follow=True)
            self.my_user.refresh_from_db()
            self.assertEqual(self.my_user.sales_amount, 0)
            self.assertEqual(self.my_user.closed_sales, 1)

    def test_statuses_changed(self):
        group_managers = Group.objects.get(name="Managers")
        self.user.groups.add(group_managers)
        for i in range(1, 6):
            self.data.update({"status": i})
            response = self.client.post(self.change_url,
                                        data=self.data,
                                        follow=True)
            self.assertEqual(response.status_code, 200)
            self.my_order.refresh_from_db()
            self.assertEqual(self.my_order.status, i)

    def test_wrong_status(self):
        group_managers = Group.objects.get(name="Managers")
        self.user.groups.add(group_managers)
        self.data.update({"status": 6})
        response = self.client.post(self.change_url,
                                    data=self.data,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.my_order.refresh_from_db()
        self.assertEqual(self.my_order.status, 1)


class OrderProductChanageTests(TestCase):

    # TODO: tests for product stock
    #  decrease / increase in case of status change
    def test_product_decreases_on_order_item_amount(self):
        pass

    def test_product_increases_on_order_item_amount(self):
        pass
