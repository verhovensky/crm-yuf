from django.test import TestCase, Client
from client.models import Client as appclientmodel
from django.urls import reverse
from datetime import datetime


# Views tests
class ClientCreationTests(TestCase):
    fixtures = ['users_and_profiles.json', 'clients.json']

    def setUp(self) -> None:
        self.client = Client()
        self.credentials = {'username': 'administrator',
                            'password': '12345'}

    def test_clients_list_authenticated(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('client:client_main'))
        self.assertEqual(response.status_code, 200)

    def test_clients_list_unauthenticated(self):
        response = self.client.get(reverse('client:client_main'))
        self.assertEqual(response.status_code, 302)

    def test_clients_detail_authenticated(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('client:client_detail',
                                           kwargs={'pk': 4,
                                                   'slug': 'gerasim'}))
        self.assertEqual(response.status_code, 200)
        btn_edit_reverse_link = reverse('client:client_edit',
                                        kwargs={'pk': 4,
                                                'slug': 'gerasim'})
        self.assertContains(response, f'<a href="{btn_edit_reverse_link}">')
        self.assertContains(response, 'button data-id="4" class="btn btn-danger get_delete_id"')
        self.assertContains(response, '<a href="javascript:history.go(-1)" class="btn btn-info">Назад</a>')

    def test_clients_detail_unauthenticated(self):
        response = self.client.get(reverse('client:client_detail', kwargs={'pk': 4,
                                                                           'slug': 'gerasim'}))
        self.assertEqual(response.status_code, 302)

    # def test_no_permission_client_view(self):
