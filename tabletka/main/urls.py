from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.get_main_page, name="main"),
    path('/auth', views.get_auth_page, name="auth"),

]