from django.test import TestCase
from django.urls import reverse
from rest_framework.reverse import reverse_lazy

from main.models import Client


class RegisterClientTests(TestCase):

    def setUp(self):
        self.username = 'client'
        self.email = 'client@client.client'
        self.first_name = 'Aboba'
        self.last_name = 'Aboba'
        self.password1 = 'Client228'
        self.password2 = 'Client228'

        self.phone = '+375295202031'
        self.address = 'ul. Aboba d.228'

    def test_register_status_code(self):
        response = self.client.get(reverse('reg_client'))
        self.assertEqual(response.status_code, 200)

    def test_signup_form(self):
        response = self.client.post(reverse('reg_client'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'phone': self.phone, 'address': self.address})

        self.assertEqual(Client.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_signup_form_failure(self):
        response = self.client.post(reverse('reg_client'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'phone': 'aboba', 'address': self.address})

        self.assertEqual(Client.objects.all().count(), 0)
