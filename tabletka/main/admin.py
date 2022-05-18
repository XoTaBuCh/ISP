from django.contrib import admin

# Register your models here.

from main.models import Client, Apothecary, Pharmacy, Medicine, Order, Product


admin.site.register(Client)
admin.site.register(Apothecary)
admin.site.register(Pharmacy)
admin.site.register(Medicine)
admin.site.register(Order)
admin.site.register(Product)

