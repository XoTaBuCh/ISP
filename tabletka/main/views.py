from concurrent.futures import ThreadPoolExecutor
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
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

        elif Apothecary.objects.filter(user_id=user.pk).exists():
            return redirect("apothecary")

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
        orders = Order.objects.filter(client__user_id=request.user.pk, status="IC")
        history = Order.objects.filter(client__user_id=request.user.pk).exclude(status="IC")

        return render(request, "client/shopping_cart.html", {"orders": orders, "history": history})

    def post(self, request):
        if not Client.objects.filter(user_id=request.user.pk).exists():
            messages.info(request, "You aren't client")
            return redirect("main")
        else:
            if request.POST.get("make_order") == "True":
                orders = Order.objects.filter(client__user_id=request.user.pk, status="IC")
                for order in orders:
                    try:
                        product = Product.objects.get(id=order.product.pk, amount__gte=order.amount)
                        if product.amount < order.amount:
                            raise Exception("So many out of stock")
                        product.amount -= order.amount
                        product.save()
                        order.status = ORDER_STATUS[1][0]
                        order.save()
                    except ObjectDoesNotExist:
                        order.status = ORDER_STATUS[3][0]
                        order.save()
                    except Exception:
                        order.status = ORDER_STATUS[3][0]
                        order.save()
            else:
                order_id = request.POST.get("order_id")
                try:
                    order = Order.objects.get(client__user_id=request.user.pk, id=order_id)
                    order.status = ORDER_STATUS[4][0]
                    order.save()
                except ObjectDoesNotExist:
                    messages.info(request, "Order doesn't exists")

        return redirect(request.path)


class ApothecaryMainView(View):
    def get(self, request):
        pharmacies_without_orders = Pharmacy.objects.filter(apothecary__user_id=request.user.pk)
        pharmacies = []
        for pharmacy in pharmacies_without_orders:
            count = Order.objects.filter(pharmacy_id=pharmacy.pk, status=ORDER_STATUS[1][0]).count()
            pharmacies.append((pharmacy, count))
        return render(request, "apothecary/apothecary_main.html", {"pharmacies": pharmacies})


class AddPharmacyView(View):
    def get(self, request):
        pharmacy_form = PharmacyForm()
        return render(request, "apothecary/add_pharmacy.html", {"pharmacy_form": pharmacy_form})

    def post(self, request):
        if not Apothecary.objects.filter(user_id=request.user.pk).exists():
            messages.info(request, "You aren't apothecary")
            return render(request, "apothecary/add_pharmacy.html", {"messages": messages})
        with ThreadPoolExecutor() as executor:
            pharmacy_thread = executor.submit(PharmacyForm, request.POST)

            pharmacy_form = pharmacy_thread.result()

        if pharmacy_form.is_valid():
            Pharmacy.objects.create(name=pharmacy_form.cleaned_data.get('name', ''),
                                    address=pharmacy_form.cleaned_data.get('address', ''),
                                    apothecary_id=request.user.apothecary.pk)
            return redirect('main')
        else:
            messages.info(request, "Incorrect data")
            return render(request, "apothecary/add_pharmacy.html", {"messages": messages})


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


class RegisterView(View):
    def get(self, request):
        user_form = UserForm()
        client_form = ClientForm()
        return render(request, 'auth/register.html', {'user_form': user_form, 'client_form': client_form})

    def post(self, request):
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


class RegisterApothecaryView(View):
    def get(self, request):
        user_form = UserForm()
        apothecary_form = ApothecaryForm()
        return render(request, 'auth/register.html', {'user_form': user_form, 'apothecary_form': apothecary_form})

    def post(self, request):
        with ThreadPoolExecutor() as executor:
            user_thread = executor.submit(UserForm, request.POST)
            apothecary_thread = executor.submit(ApothecaryForm, request.POST)

            user_form = user_thread.result()
            apothecary_form = apothecary_thread.result()

        if User.objects.filter(username=request.POST.get('username')).exists():
            messages.error(request, 'This username already registered on site.')
            return redirect('reg_apothecary')

        if user_form.is_valid() and apothecary_form.is_valid():
            new_user = user_form.save()
            apothecary_new = Apothecary.objects.create(user=new_user)
            apothecary_new.save()
            return redirect('auth')
        else:
            messages.error(request, 'Your data is incorrect')
            return redirect('reg_client')


class MedicineView(View):
    def get(self, request, medicine_id):
        medicine = Medicine.objects.get(pk=medicine_id)
        products = Product.objects.filter(medicine_id=medicine_id)
        client_flag = Client.objects.filter(user_id=request.user.pk).exists()
        return render(request, "medicine/medicine.html",
                      {"medicine": medicine, "products": products, "client_flag": client_flag})

    def post(self, request, medicine_id):
        if not Client.objects.filter(user_id=request.user.pk).exists():
            messages.info(request, "You aren't client")
            print(3)
        else:
            product_id = request.POST.get("product_id")
            product = Product.objects.get(id=product_id)
            with ThreadPoolExecutor() as executor:
                order_thread = executor.submit(OrderForm, request.POST)

                order_form = order_thread.result()

            if order_form.is_valid():
                amount = order_form.cleaned_data.get("amount")
                price = amount * product.price
                if product.amount > amount:
                    Order.objects.create(amount=amount, price=price, client_id=request.user.client.pk,
                                         pharmacy_id=product.pharmacy_id, product_id=product_id)
                else:
                    messages.info(request, "So many out of stock")
            else:
                messages.info(request, "Incorrect data")

        return redirect(request.path)


class PharmacyView(View):
    def get(self, request, pharmacy_id):
        pharmacy = Pharmacy.objects.get(pk=pharmacy_id)
        products = Product.objects.filter(pharmacy_id=pharmacy_id)
        apothecary_flag = (request.user.pk == pharmacy.apothecary.user.pk)

        return render(request, "pharmacy/pharmacy.html",
                      {"pharmacy": pharmacy, "products": products, "apothecary_flag": apothecary_flag})

    def post(self, request, pharmacy_id):
        if not Pharmacy.objects.filter(apothecary__user_id=request.user.pk).exists():
            messages.info(request, "You aren't apothecary")
        else:
            product_id = request.POST.get("product_id")
            try:
                product = Product.objects.get(id=product_id, pharmacy_id=pharmacy_id)
                with ThreadPoolExecutor() as executor:
                    product_thread = executor.submit(ProductForm, request.POST)

                    product_form = product_thread.result()

                if product_form.is_valid():
                    product.price = product_form.cleaned_data.get("price")
                    product.amount = product_form.cleaned_data.get("amount")
                    product.save()
                else:
                    messages.info(request, "Wrong data")

            except ObjectDoesNotExist:
                messages.info(request, "Product doesn't exists")

            return redirect(request.path)


class PharmacyOrderView(View):
    def get(self, request, pharmacy_id):
        orders = Order.objects.filter(pharmacy_id=pharmacy_id, status=ORDER_STATUS[1][0])
        return render(request, "pharmacy/orders.html", {"orders": orders})

    def post(self, request, pharmacy_id):
        if not Pharmacy.objects.filter(apothecary__user_id=request.user.pk).exists():
            messages.info(request, "You aren't apothecary")
        else:
            try:
                order_id = request.POST.get("order_id")
                order = Order.objects.get(pharmacy_id=pharmacy_id, id=order_id)
                order.status = ORDER_STATUS[2][0]
                order.save()
            except ObjectDoesNotExist:
                messages.info(request, "Order doesn't exists")

        return redirect(request.path)
