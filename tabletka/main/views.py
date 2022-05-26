from concurrent.futures import ThreadPoolExecutor
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max, Min
from django.http import HttpResponseRedirect

from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DetailView, RedirectView, ListView, CreateView
from django.views.generic.edit import FormMixin
from search_views.filters import BaseFilter
from search_views.views import SearchListView

from .models import *
from django.contrib.auth import logout, login, authenticate
from .forms import *
import logging

logger = logging.getLogger(__name__)


class MedicineFilter(BaseFilter):
    search_fields = {
        'request': ['name', 'description', 'fabricator'],
    }


class MainView(RedirectView):
    logger.info("Main")

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return reverse_lazy("home")

        if Client.objects.filter(user_id=user.pk).exists():
            url = reverse_lazy("client")

        elif Apothecary.objects.filter(user_id=user.pk).exists():
            url = reverse_lazy("apothecary")

        elif user.is_superuser:
            url = reverse_lazy("admin:index")

        else:
            url = reverse_lazy("home")

        return url


class HomeView(SearchListView):
    logger.info("Home")
    template_name = "main/main.html"
    model = Medicine
    form_class = MedicineSearchForm
    filter_class = MedicineFilter
    context_object_name = "medicines"


class ClientMainView(SearchListView):
    logger.info("Client Main")
    template_name = "client/client_main.html"
    model = Medicine
    form_class = MedicineSearchForm
    filter_class = MedicineFilter
    context_object_name = "medicines"


class ClientCartView(View):

    def get(self, request):
        orders = Order.objects.filter(client__user_id=request.user.pk, status=ORDER_STATUS[0][0])
        history = Order.objects.filter(client__user_id=request.user.pk).exclude(status=ORDER_STATUS[0][0])

        return render(request, "client/shopping_cart.html", {"orders": orders, "history": history})

    def post(self, request):
        if not Client.objects.filter(user_id=request.user.pk).exists():
            messages.info(request, "You aren't client")
            return redirect("main")
        else:
            if request.POST.get("make_order") == "True":
                orders = Order.objects.filter(client__user_id=request.user.pk, status=ORDER_STATUS[0][0])
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


class ApothecaryMainView(ListView):
    logger.info("Apothecary Main")
    model = Pharmacy
    template_name = "apothecary/apothecary_main.html"
    context_object_name = "pharmacies"

    def get_queryset(self):
        pharmacies_without_orders = Pharmacy.objects.filter(apothecary__user_id=self.request.user.pk)
        pharmacies = []
        for pharmacy in pharmacies_without_orders:
            count = Order.objects.filter(pharmacy_id=pharmacy.pk, status=ORDER_STATUS[1][0]).count()
            pharmacies.append((pharmacy, count))
        return pharmacies


class AddPharmacyView(CreateView):
    logger.info("Add pharmacy")
    template_name = "apothecary/add_pharmacy.html"
    form_class = PharmacyForm

    def form_valid(self, form):
        pharmacy = form.save(commit=False)
        pharmacy.apothecary = self.request.user.apothecary
        pharmacy.save()
        messages.info(self.request, "New pharmacy added successful")
        return HttpResponseRedirect(reverse_lazy("main"))


class MedicineView(DetailView):
    logger.info("Medicine")
    template_name = "medicine/medicine.html"
    model = Medicine
    context_object_name = "medicine"
    pk_url_kwarg = "medicine_id"

    def get_context_data(self, **kwargs):
        context = super(MedicineView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(medicine_id=self.kwargs["medicine_id"])
        context['client_flag'] = Client.objects.filter(user_id=self.request.user.pk).exists()

        return context


class MakeOrderView():
    pass

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


class PharmacyAddProductView(View):
    def get(self, request, pharmacy_id):
        medicines = Medicine.objects.all();
        medicine_form = MedicineForm()
        product_form = ProductForm()

        return render(request, "pharmacy/add_product.html",
                      {"medicines": medicines, "medicine_form": medicine_form, "product_form": product_form,
                       "types": MEDICINE_TYPES})


class ProfileView(SuccessMessageMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = "main/profile.html"
    success_message = "Successfully Changed Your Profile"
    success_url = reverse_lazy('main')

    def get_object(self):
        return Client.objects.get(user_id=self.request.user.pk)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'main/change_password.html'
    form_class = PasswordChangeForm
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('main')
