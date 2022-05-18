from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


USER_STATUS = ["ACTIVE",
               "BANNED"
               ]
MEDICINE_TYPES = ["PILLS",
                  "CAPSULES",
                  "POWDERS",
                  "SYRUP",
                  "MIXTURE",
                  "OINTMENT"
                  ]
ORDER_STATUS = ["DONE",
                "ACTIVE",
                "CANCELED"]


class Client(models.Model):
    #user = models.OneToOneField(User, on_delete=models.PROTECT)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    address = models.TextField(blank=True, null=True)
    status = models.TextChoices("Status", USER_STATUS)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.first_name


class Apothecary(models.Model):
    first_name = models.CharField("First name", max_length=255)
    last_name = models.CharField("Last name", max_length=255)
    email = models.EmailField()
    password = models.CharField("Password", max_length=255)
    status = models.TextChoices("Status", USER_STATUS)
    createdAt = models.DateTimeField("Created At", auto_now_add=True)

    def __str__(self):
        return self.first_name


class Medicine(models.Model):
    name = models.CharField("Name", max_length=255)
    description = models.TextField("Description", blank=True)
    fabricator = models.TextField("Fabricator", blank=True)
    type = models.TextChoices("Type", MEDICINE_TYPES)
    date_created = models.DateTimeField(auto_now_add=True)

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
    amount = models.IntegerField("Amount")
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)


class Order(models.Model):
    price = models.DecimalField("Price", max_digits=10, decimal_places=2)
    amount = models.IntegerField("Amount")
    status = models.TextChoices("Status", ORDER_STATUS)
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
