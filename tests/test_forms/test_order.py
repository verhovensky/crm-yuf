from django.test import TestCase
from datetime import datetime, timedelta
from tests.factories.clients import ClientFactory
from order.forms import OrderCreateForm, OrderChangeForm
from tests.factories.users import UserFactory


class OrderCreateFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.future_date = datetime.now() + \
                          timedelta(days=2, seconds=852)
        cls.client = ClientFactory.create(created_by=cls.user)
        cls.data = {"this_order_client": cls.client.pk,
                    "full_name": "Che Guarana",
                    "address": "Data street, 18, 1",
                    "phone": "79874573851",
                    "delivery_time": cls.future_date,
                    "self_pick": True,
                    "cash_on_delivery": True,
                    "description": "Random string",
                    "new_client": False,
                    "for_other": False}

    def test_for_client_correct_date(self):
        form = OrderCreateForm(data=self.data)
        self.assertEqual(form.errors, {})

    def test_for_client_wrong_date(self):
        new_data = self.data.copy()
        past_time = datetime.now() - timedelta(seconds=852)
        new_data.update({"delivery_time": past_time})
        form = OrderCreateForm(data=new_data)
        self.assertEqual(form.errors["delivery_time"],
                         ["Нельзя указать дату в прошлом!"])

    def test_for_client_wrong_phone(self):
        phone_error = "Телефон должен быть в формате: +7926783645 " \
                      "Макс. длинна = 16 знаков"
        new_data = self.data.copy()
        new_data.update({"phone": "myphone"})
        form = OrderCreateForm(data=new_data)
        self.assertEqual(form.errors["phone"], [phone_error])
        new_data.update({"phone": "698746163758"})
        self.assertEqual(form.errors["phone"], [phone_error])
        new_data.update({"phone": "6" * 17})
        self.assertEqual(form.errors["phone"], [phone_error])

    def test_for_client_no_client(self):
        new_data = self.data.copy()
        new_data.pop("this_order_client")
        form = OrderCreateForm(data=new_data)
        self.assertEqual(form.errors["this_order_client"],
                         ["Это поле обязательно!"])

    def test_new_client(self):
        new_data = self.data.copy()
        new_data.pop("this_order_client")
        new_data.update({"new_client": True})
        form = OrderCreateForm(data=new_data)
        self.assertNotIn("this_order_client", form.data)
        self.assertEqual(form.errors, {})

    def test_for_other(self):
        new_data = self.data.copy()
        new_data.update({"for_other": True})
        form = OrderCreateForm(data=new_data)
        self.assertEqual(form.errors, {})


class OrderChangeFormTests(TestCase):

    def test_order_change_status(self):
        for i in range(1, 6):
            form = OrderChangeForm(data={"status": i})
            self.assertEqual(form.errors, {})

    def test_form_fields(self):
        form = OrderChangeForm()
        form_fields = ("full_name", "address", "phone",
                       "status", "description")
        for i in form_fields:
            self.assertIn(i, form.fields)

    # TODO:
    # def test_full_name_length(self):
    #     pass
    #
    # def test_phone_regex(self):
    #     pass
    #
    # def test_address_length(self):
    #     pass
