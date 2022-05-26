from django.urls import path

from .views import *

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('home', HomeView.as_view(), name="home"),
    path('profile', ProfileView.as_view(), name="profile"),
    path('profile/change_password', ChangePasswordView.as_view(), name="change_password"),
    path('client', ClientMainView.as_view(), name="client"),
    path('client/shopping_cart', ClientCartView.as_view(), name="shopping_cart"),
    path('apothecary', ApothecaryMainView.as_view(), name="apothecary"),
    path('apothecary/add_pharmacy', AddPharmacyView.as_view(), name="add_pharmacy"),

    path('medicine/<int:medicine_id>/', MedicineView.as_view(), name="medicine"),
    path('medicine/<int:medicine_id>/make_order', MakeOrderView.as_view(), name="make_order"),
    path('pharmacy/<int:pharmacy_id>/', PharmacyView.as_view(), name="pharmacy"),
    path('pharmacy/<int:pharmacy_id>/orders', PharmacyOrderView.as_view(), name="pharmacy_order"),
    path('pharmacy/<int:pharmacy_id>/add_product', PharmacyAddProductView.as_view(), name="pharmacy_add_product"),

]