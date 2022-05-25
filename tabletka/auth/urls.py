from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import *

urlpatterns = [
    path('', AuthView.as_view(), name="auth"),
    path('register', RegisterView.as_view(), name="reg_client"),
    path('register_apothecary', RegisterApothecaryView.as_view(), name="reg_apothecary"),
    path('login', MyLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
