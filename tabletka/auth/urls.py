from django.contrib.auth.views import LogoutView
from django.urls import path, re_path

from .views import *

urlpatterns = [
    path('', AuthView.as_view(), name="auth"),
    path('register', RegisterView.as_view(), name="reg_client"),
    path('register_apothecary', RegisterApothecaryView.as_view(), name="reg_apothecary"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z\-]{1,50})/$', ActivateView.as_view(),
            name='activate'),
    path('login', MyLoginView.as_view(), name="login"),
    path('logout', LogoutView.as_view(), name="logout"),
]
