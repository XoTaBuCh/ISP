from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from main.models import Client, Apothecary, Pharmacy, Product, Medicine, Order


class MainTests(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='client', email='client@client.client', first_name='Aboba',
                                        last_name='Aboba', password='Qwerty228')
        self.client.force_login(self.user)

    def test_main_code(self):
        self.client_x = Client.objects.create(user=self.user, phone='+375295202031', address='ul. Aboba d.228')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 302)

    def test_main_code2(self):
        self.apothecary_x = Apothecary.objects.create(user=self.user, about_education='BGMU', experience='3')
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 302)

    def test_main_code3(self):
        response = self.client.get(reverse('main'))
        self.assertEqual(response.status_code, 302)


class ApothecaryMainTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='client', email='client@client.client', first_name='Aboba',
                                        last_name='Aboba', password='Qwerty228')
        self.client.force_login(self.user)
        self.apothecary_x = Apothecary.objects.create(user=self.user, about_education='BGMU', experience='3')
        self.pharmacy = Pharmacy.objects.create(apothecary=self.apothecary_x, name="Pharmacy 1", address="ulica clown")

    def test_main_code(self):
        response = self.client.get(reverse('apothecary'))
        self.assertEqual(response.status_code, 200)

    def test_add_pharmacy_code(self):
        response = self.client.get(reverse('add_pharmacy'))
        self.assertEqual(response.status_code, 200)

    def test_add_pharmacy_post_code(self):
        response = self.client.post(reverse('add_pharmacy'), {'name': "Pharmcay 2", 'address': "per Abob"})
        self.assertEqual(Pharmacy.objects.all().count(), 2)
        self.assertEqual(response.status_code, 302)

    def test_add_pharmacy_post_fail_code(self):
        response = self.client.post(reverse('add_pharmacy'), {'name': "", 'address': "per Abob"})
        self.assertEqual(Pharmacy.objects.all().count(), 1)

    def test_profile_code(self):
        response = self.client.post(reverse('profile'), {'about_education': "4 classes", 'experience': "9"})
        self.assertEqual(response.status_code, 302)

    def test_add_product_code(self):
        response = self.client.post(reverse('add_product', kwargs={'pharmacy_id': self.pharmacy.pk}),
                                    {'name': "aboba1", 'description': "aboba1", 'fabricator': "aboba1", 'type': "PILLS",
                                     'image': "", 'amount': "5", 'price': "40"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_add_existing_product_code(self):
        Medicine.objects.create(name="aboba1", description="aboba1", fabricator="aboba1", type="PILLS", image="")
        response = self.client.post(reverse('add_existing_product', kwargs={'pharmacy_id': self.pharmacy.pk}),
                                    {'amount': "5", 'price': "40", 'medicine_id': "1"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Product.objects.all().count(), 1)

    def test_add_existing_product_get_code(self):
        Medicine.objects.create(name="aboba1", description="aboba1", fabricator="aboba1", type="PILLS", image="")
        response = self.client.get(reverse('add_existing_product', kwargs={'pharmacy_id': self.pharmacy.pk}))
        self.assertEqual(response.status_code, 200)


class ClientMainTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='client', email='client@client.client', first_name='Aboba',
                                        last_name='Aboba', password='Qwerty228')
        self.client.force_login(self.user)
        self.client_x = Client.objects.create(user=self.user, address='Abobnaya', phone='+375336103444')
        self.medicine = Medicine.objects.create(name="aboba1", description="aboba1", fabricator="aboba1", type="PILLS")

        self.user_x = User.objects.create(username='apothecary', email='client@client.client', first_name='Aboba',
                                          last_name='Aboba', password='Qwerty228')
        self.apothecary_x = Apothecary.objects.create(user=self.user_x, about_education='BGMU', experience='3')
        self.pharmacy = Pharmacy.objects.create(apothecary=self.apothecary_x, name="Pharmacy 1", address="ulica clown")
        self.product = Product.objects.create(amount="100", price="1", medicine=self.medicine, pharmacy=self.pharmacy)

    def test_main_code(self):
        response = self.client.get(reverse('client'))
        self.assertEqual(response.status_code, 200)

    def test_medicine_code(self):
        response = self.client.get(reverse('medicine', kwargs={'medicine_id': "2"}))
        self.assertEqual(response.status_code, 200)

    def test_product_get_code(self):
        response = self.client.get(reverse('make_order', kwargs={'product_id': "2"}))
        self.assertEqual(response.status_code, 200)

    def test_product_get_code(self):
        response = self.client.post(reverse('make_order', kwargs={'product_id': "2"}), {'amount': "1"})
        self.assertEqual(response.status_code, 302)

    def test_product_get_fail_code(self):
        response = self.client.post(reverse('make_order', kwargs={'product_id': "2"}), {'amount': "dgsfg"})
        self.assertEqual(response.status_code, 200)
