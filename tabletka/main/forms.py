from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as trans

from .models import *


class UserForm(UserCreationForm):
    username = forms.CharField(label="Username", required=True)
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label="Repeat password", widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ["username", "email", 'password1', 'password2', 'first_name', 'last_name']


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["phone", "address"]


class ApothecaryForm(forms.ModelForm):
    class Meta:
        model = Apothecary
        fields = ["about_education", "experience"]


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "description", "fabricator", "type", "image"]


class PharmacyForm(forms.ModelForm):
    class Meta:
        model = Pharmacy
        fields = ["name", "address"]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["price", "amount"]


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["amount"]


class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['phone', 'address']


class MedicineSearchForm(forms.Form):
    request = forms.CharField(required=False)
