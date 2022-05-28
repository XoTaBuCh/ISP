from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Client, Apothecary


class RegisterClientTests(TestCase):

    def setUp(self):
        self.username = 'client'
        self.email = 'client@client.client'
        self.first_name = 'Aboba'
        self.last_name = 'Aboba'
        self.password1 = 'Qwerty228'
        self.password2 = 'Qwerty228'

        self.phone = '+375295202031'
        self.address = 'ul. Aboba d.228'

    def test_register_status_code(self):
        response = self.client.get(reverse('reg_client'))
        self.assertEqual(response.status_code, 200)

    def test_register_form(self):
        response = self.client.post(reverse('reg_client'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'phone': self.phone, 'address': self.address})

        self.assertEqual(Client.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_register_form_fail(self):
        response = self.client.post(reverse('reg_client'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'phone': 'aboba', 'address': self.address})

        self.assertEqual(Client.objects.all().count(), 0)


class RegisterApothecaryTests(TestCase):

    def setUp(self):
        self.username = 'apothecary'
        self.email = 'apothecary@apothecary.apothecary'
        self.first_name = 'Aboba'
        self.last_name = 'Aboba'
        self.password1 = 'Qwerty228'
        self.password2 = 'Qwerty228'

        self.about_education = 'BGMU'
        self.experience = '3'

    def test_register_apothecary_status_code(self):
        response = self.client.get(reverse('reg_apothecary'))
        self.assertEqual(response.status_code, 200)

    def test_register_apothecary_form(self):
        response = self.client.post(reverse('reg_apothecary'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'about_education': self.about_education,
                                     'experience': self.experience})

        self.assertEqual(Apothecary.objects.all().count(), 1)
        self.assertEqual(response.status_code, 302)

    def test_register_apothecary_form_fail(self):
        response = self.client.post(reverse('reg_apothecary'),
                                    {'username': self.username, 'email': self.email, 'first_name': self.first_name,
                                     'last_name': self.last_name, 'password1': self.password1,
                                     'password2': self.password2, 'about_education': self.about_education,
                                     'experience': "aboba"})

        self.assertEqual(Apothecary.objects.all().count(), 0)


class LoginTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='client', email='client@client.client', first_name='Aboba',
                                        last_name='Aboba', password='Qwerty228')
        self.client.force_login(self.user)

        self.client_x = Client.objects.create(user=self.user, phone='+375295202031', address='ul. Aboba d.228')

    def test_auth_status_code(self):
        response = self.client.get(reverse('auth'))
        self.assertEqual(response.status_code, 200)

    def test_logout_status_code(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
