from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as trans

from .models import *


class UserForm(forms.ModelForm):
    error_messages = {
        'password_mismatch': trans("The two password fields didn't match."),
    }
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)

    class Meta:
        model = User
        fields = ["username", "email", 'password1', 'password2', 'first_name', 'last_name']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["phone", "address"]


class ApothecaryForm(forms.ModelForm):
    class Meta:
        model = Apothecary
        fields = []


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

