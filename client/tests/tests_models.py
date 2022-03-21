from django.test import TestCase
from datetime import datetime
from client.models import Client


# Models tests
class ClientCreationTests(TestCase):
    fixtures = ['users_and_profiles.json']

    def setUp(self) -> None:
        self.example_client = Client.objects.create(name='Андрей Денисов',
                                     slug='andrej-denisov',
                                     phone_number='+79265674567',
                                     type='IND',
                                     origin='MAIL',
                                     email='andrej@gmail.com')

    def test_create_client(self):
        self.assertIsInstance(self.example_client, Client)
        self.assertIsInstance(self.example_client.created, datetime)
        self.assertIsInstance(self.example_client.updated, datetime)
        self.assertEqual(self.example_client.name, 'Андрей Денисов')
        self.assertEqual(self.example_client.slug, 'andrej-denisov')
        self.assertEqual(self.example_client.phone_number, '+79265674567')
        self.assertEqual(self.example_client.type, 'IND')
        self.assertEqual(self.example_client.origin, 'MAIL')
        self.assertEqual(self.example_client.email, 'andrej@gmail.com')
        self.assertEqual(str(self.example_client), 'Андрей Денисов')

    def test_str(self):
        self.assertEqual(str(self.example_client), 'Андрей Денисов')

    def test_created_by(self):
        self.assertEqual(self.example_client.created_by_id, 1)

    # def test_client_delete(self):

    # def test_client_update(self):
