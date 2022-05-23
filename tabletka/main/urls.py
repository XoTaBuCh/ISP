from django.urls import path, re_path, include
from . import views
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('client', ClientMainView.as_view(), name="client"),
    path('client/shopping_cart', ClientCartView.as_view(), name="shopping_cart"),
    path('apothecary', ApothecaryMainView.as_view(), name="apothecary"),
    path('apothecary/add_pharmacy', AddPharmacyView.as_view(), name="add_pharmacy"),

    path('auth', AuthView.as_view(), name="auth"),
    path('auth/register', RegisterView.as_view(), name="reg_client"),
    path('auth/register_apothecary', RegisterApothecaryView.as_view(), name="reg_apothecary"),
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),

    path('medicine/<int:medicine_id>/', MedicineView.as_view(), name="medicine"),
    path('pharmacy/<int:pharmacy_id>/', PharmacyView.as_view(), name="pharmacy"),
    path('pharmacy/<int:pharmacy_id>/orders', PharmacyOrderView.as_view(), name="pharmacy_order")

]