from django.urls import path, re_path, include
from . import views
from .views import *

urlpatterns = [
    path('', MainView.as_view(), name="main"),
    path('client', ClientMainView.as_view(), name="client"),

    path('auth', AuthView.as_view(), name="auth"),
    path('auth/register', views.get_client_reg_page, name="reg_client"),
    path('auth/login', LoginView.as_view(), name="login"),
    path('auth/logout', LogoutView.as_view(), name="logout"),

    re_path(r'^medicine/(?P<medicine_id>\d+)/$', views.medicine_specific, name='medicine'),
    re_path(r'^pharmacy/(?P<pharmacy_id>\d+)/$', views.pharmacy_specific, name='pharmacy'),

]