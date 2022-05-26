from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from phonenumber_field.modelfields import PhoneNumberField

MEDICINE_TYPES = [("PILLS", "PILLS"),
                  ("CAPSULES", "CAPSULES"),
                  ("POWDERS", "POWDERS"),
                  ("SYRUP", "SYRUP"),
                  ("MIXTURE", "MIXTURE"),
                  ("OINTMENT", "OINTMENT")]
ORDER_STATUS = [("IN CART", "IN CART"),
                ("ACTIVE", "ACTIVE"),
                ("DONE", "DONE"),
                ("CANCELED", "CANCELED"),
                ("DELETED", "DELETED")]


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    phone = PhoneNumberField()
    address = models.TextField(blank=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)


class Apothecary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    about_education = models.TextField(blank=True)
    experience = models.PositiveIntegerField("Experience", blank=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)


class Medicine(models.Model):
    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True)
    fabricator = models.TextField("Fabricator", blank=True)
    type = models.CharField("Type", max_length=10, choices=MEDICINE_TYPES, default=MEDICINE_TYPES[0][0])
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField("Image", blank=True, upload_to="medicines")


class Pharmacy(models.Model):
    name = models.CharField("Name", max_length=255)
    address = models.TextField("Address", blank=True)
    apothecary = models.ForeignKey(Apothecary, on_delete=models.CASCADE)


class Product(models.Model):
    price = models.DecimalField("Price", max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    amount = models.PositiveIntegerField("Amount")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)


class Order(models.Model):
    price = models.DecimalField("Price", max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(Decimal('0.01'))])
    amount = models.PositiveIntegerField("Amount", validators=[MinValueValidator(1)])
    status = models.CharField("Status", max_length=10, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
