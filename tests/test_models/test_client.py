from django.test import TestCase
from client.models import Client
from tests.factories.clients import ClientFactory
from tests.factories.users import UserFactory
from django.db.utils import IntegrityError


class ClientCreateTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory.create()
        cls.my_user = UserFactory.create(
            user=cls.user)

    def test_create_client(self):
        client = ClientFactory.create(
            created_by=self.my_user)
        self.assertIsInstance(client.phone_number, str)
        self.assertIsInstance(client.name, str)
        self.assertIsInstance(client.email, str)
        self.assertIn("@", client.email)
        self.assertIsInstance(client.type, int)
        self.assertIsInstance(client.origin, int)

    def test_update_client(self):
        pass

    def tes_delete_client(self):
        pass

    def test_create_batch(self):
        clients = ClientFactory.create_batch(
            size=5,
            created_by=self.my_user)
        self.assertEqual(len(clients), 5)
        for i, j in enumerate(clients[:-1]):
            i = i + 1
            if len(clients) > i:
                self.assertNotEqual(j.phone_number,
                                    clients[i].phone_number)
                self.assertNotEqual(j.name,
                                    clients[i].name)
                self.assertNotEqual(j.email,
                                    clients[i].email)

    def test_unique_phone_number(self):
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                phone_number="7926785432")
            Client.objects.create(
                phone_number="7926785432")

    def test_unique_name(self):
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                name="Alexander Siksalandyr")
            Client.objects.create(
                name="Alexander Siksalandyr")

    def test_unique_email(self):
        with self.assertRaises(IntegrityError):
            Client.objects.create(
                email="siksalandyr@gmail.com")
            Client.objects.create(
                email="siksalandyr@gmail.com")
