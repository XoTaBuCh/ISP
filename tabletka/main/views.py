from concurrent.futures import ThreadPoolExecutor
from django.contrib import messages
from django.db.models import Max, Min

from django.shortcuts import render, redirect
from django.views import View

from .models import *
from django.contrib.auth import logout, login, authenticate
from .forms import *
import logging

logger = logging.getLogger(__name__)


class MainView(View):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return render(request, "main/main.html")

        if Client.objects.filter(user_id=user.pk).exists():
            return redirect("client")

        elif Apothecary.objects.filter():
            return redirect("")

        else:
            return render(request, "main/main.html")

    def post(self, request):
        medicines = Medicine.objects.filter(name__contains=request.POST.get("request"))
        for medicine in medicines:
            medicine.min_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Min("price"))["price__min"]
            medicine.max_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Max("price"))["price__max"]

        return render(request, "main/main.html", {"medicines": medicines})


class ClientMainView(View):
    def get(self, request):
        return render(request, "client/client_main.html")

    def post(self, request):
        medicines = Medicine.objects.filter(name__contains=request.POST.get("request"))
        for medicine in medicines:
            medicine.min_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Min("price"))["price__min"]
            medicine.max_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Max("price"))["price__max"]

        return render(request, "client/client_main.html", {"medicines": medicines})


class ClientCartView(View):
    def get(self, request):
        return render(request, "client/client_main.html")

    def post(self, request):
        medicines = Medicine.objects.filter(name__contains=request.POST.get("request"))
        for medicine in medicines:
            medicine.min_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Min("price"))["price__min"]
            medicine.max_price = Product.objects.filter(medicine_id=medicine.pk).aggregate(Max("price"))["price__max"]

        return render(request, "client/client_main.html", {"medicines": medicines})


class LoginView(View):
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('main')
        else:
            messages.info(request, 'Username or password is not correct')
        return render(request, 'auth/login.html', {})

    def get(self, request):
        return render(request, 'auth/login.html')


class LogoutView(View):
    def get(self, request):
        user = request.user

        if user.is_authenticated:
            logout(request)

        return redirect('main')


class AuthView(View):
    def get(self, request):
        return render(request, "auth/auth.html")


def medicine_specific(request, medicine_id):
    medicine = Medicine.objects.get(pk=medicine_id)
    products = Product.objects.filter(medicine_id=medicine_id)
    return render(request, "medicine/medicine.html", {"medicine": medicine, "products": products})


def get_client_reg_page(request):
    if request.method == "GET":
        user_form = UserForm()
        client_form = ClientForm()
        return render(request, 'auth/register.html', {'user_form': user_form, 'client_form': client_form})
    else:
        with ThreadPoolExecutor() as executor:
            user_thread = executor.submit(UserForm, request.POST)
            client_thread = executor.submit(ClientForm, request.POST)

            user_form = user_thread.result()
            client_form = client_thread.result()

        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'This username already registered on site.')
            return redirect('reg_client')

        if user_form.is_valid() and client_form.is_valid():
            new_user = user_form.save()
            client_new = Client.objects.create(user=new_user)
            client_new.phone_number = client_form.cleaned_data.get('phone', '')
            client_new.address = client_form.cleaned_data.get('address', '')
            client_new.save()
            return redirect('auth')
        else:
            messages.error(request, 'Your data is incorrect')
            return redirect('reg_client')


def pharmacy_specific(request):
    return None
