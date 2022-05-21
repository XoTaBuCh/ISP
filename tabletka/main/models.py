from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


MEDICINE_TYPES = [("PL", "PILLS"),
                  ("CP", "CAPSULES"),
                  ("PW", "POWDERS"),
                  ("SR", "SYRUP"),
                  ("MX", "MIXTURE"),
                  ("ON", "OINTMENT")]
ORDER_STATUS = [("AC", "ACTIVE"),
                ("DN", "DONE"),
                ("CN", "CANCELED")]


class Client(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)


class Apothecary(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, blank=True)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)


class Medicine(models.Model):
    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True)
    fabricator = models.TextField("Fabricator", blank=True)
    type = models.CharField("Type", max_length=2, choices=MEDICINE_TYPES, default=MEDICINE_TYPES[0][0])
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField("Image", blank=True, upload_to="medicines")

    min_price = models.DecimalField("Min price", max_digits=10, decimal_places=2, default=0)
    max_price = models.DecimalField("Max price", max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class Pharmacy(models.Model):
    name = models.CharField("Name", max_length=255)
    address = models.TextField("Address", blank=True)
    apothecary = models.ForeignKey(Apothecary, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Product(models.Model):
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField("Amount")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)


class Order(models.Model):
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    amount = models.PositiveIntegerField("Amount")
    status = models.CharField("Status", max_length=2, choices=ORDER_STATUS, default=ORDER_STATUS[0][0])
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
