import logging

from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DetailView, RedirectView, ListView, CreateView
from django.views.generic.edit import FormMixin
from search_views.filters import BaseFilter
from search_views.views import SearchListView

from .forms import *

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
        logger.info("Shopping cart GET")
        orders = Order.objects.filter(client__user_id=request.user.pk, status=ORDER_STATUS[0][0])
        actives = Order.objects.filter(client__user_id=request.user.pk, status=ORDER_STATUS[1][0])
        history = Order.objects.filter(client__user_id=request.user.pk).exclude(
            Q(status=ORDER_STATUS[0][0]) | Q(status=ORDER_STATUS[1][0]))

        return render(request, "client/shopping_cart.html", {"orders": orders, "actives": actives, "history": history})

    def post(self, request):
        logger.info("Shopping cart POST")
        if not Client.objects.filter(user_id=request.user.pk).exists():
            messages.info(request, "You aren't client")
            return redirect("main")
        else:
            if request.POST.get("flag") == "1":
                orders = Order.objects.filter(client__user_id=request.user.pk, status=ORDER_STATUS[0][0])
                for order in orders:
                    try:
                        product = Product.objects.get(id=order.product.pk, amount__gte=order.amount)
                        product.amount -= order.amount
                        product.save()
                        order.status = ORDER_STATUS[1][0]
                        order.save()
                    except ObjectDoesNotExist:
                        order.status = ORDER_STATUS[3][0]
                        order.save()
            elif request.POST.get("flag") == "2":
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


class MakeOrderView(DetailView, FormMixin):
    logger.info("Make order")
    template_name = "medicine/make_order.html"
    form_class = OrderForm
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    success_url = reverse_lazy("shopping_cart")

    def get_context_data(self, **kwargs):
        ctx = super(MakeOrderView, self).get_context_data(**kwargs)
        ctx["form"] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.cleaned_data.get("amount") > self.object.amount:
            messages.info(self.request, "Out of stocks")
            return super(MakeOrderView, self).form_invalid(form)
        else:
            order = form.save(commit=False)
            order.status = ORDER_STATUS[0][0]
            order.pharmacy = self.object.pharmacy
            order.client = self.request.user.client
            order.product = self.object
            order.price = order.amount * self.object.price
            order.save()
            messages.info(self.request, "Added to cart")
        return super(MakeOrderView, self).form_valid(form)


class PharmacyView(DetailView):
    logger.info("Pharmacy")
    template_name = "pharmacy/pharmacy.html"
    model = Pharmacy
    context_object_name = "pharmacy"
    pk_url_kwarg = "pharmacy_id"

    def get_context_data(self, **kwargs):
        context = super(PharmacyView, self).get_context_data(**kwargs)
        context['products'] = Product.objects.filter(pharmacy_id=self.kwargs["pharmacy_id"])
        context['apothecary_flag'] = Apothecary.objects.filter(user_id=self.request.user.pk).exists()

        return context


class PharmacyEditProductView(DetailView, FormMixin):
    logger.info("Edit product")
    template_name = "pharmacy/edit_product.html"
    form_class = ProductForm
    model = Product
    context_object_name = "product"
    pk_url_kwarg = "product_id"

    def get_success_url(self):
        return reverse_lazy("pharmacy", kwargs={'pharmacy_id': self.object.pharmacy.pk})

    def get_context_data(self, **kwargs):
        ctx = super(PharmacyEditProductView, self).get_context_data(**kwargs)
        ctx["form"] = self.get_form()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object.amount = form.cleaned_data.get("amount")
        self.object.price = form.cleaned_data.get("price")
        self.object.save()
        messages.info(self.request, "Edited")
        return super(PharmacyEditProductView, self).form_valid(form)


class PharmacyOrderView(ListView):
    logger.info("Pharmacy order")
    template_name = "pharmacy/orders.html"
    model = Order
    context_object_name = "orders"
    pk_url_kwarg = "pharmacy_id"

    def get_queryset(self):
        return Order.objects.filter(pharmacy_id=self.kwargs["pharmacy_id"], status=ORDER_STATUS[1][0])

    def post(self, request):
        if not Pharmacy.objects.filter(apothecary__user_id=request.user.pk).exists():
            messages.info(request, "You aren't apothecary")
        else:
            try:
                order_id = request.POST.get("order_id")
                order = Order.objects.get(pharmacy_id=self.kwargs["pharmacy_id"], id=order_id)
                if request.POST.get("flag") == "True":
                    order.status = ORDER_STATUS[2][0]
                else:
                    order.status = ORDER_STATUS[3][0]
                order.save()
            except ObjectDoesNotExist:
                messages.info(request, "Order doesn't exists")

        return redirect(request.path)


class PharmacyAddProductView(CreateView):
    logger.info("Add Product")
    template_name = "pharmacy/add_product.html"
    form_class = MedicineForm

    def get_context_data(self, **kwargs):
        context = super(PharmacyAddProductView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = ProductForm(self.request.POST)
            context['form_medicine'] = MedicineForm(self.request.POST)
        else:
            context['form'] = ProductForm()
            context['form_medicine'] = MedicineForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_product = context['form']
        if form_product.is_valid():
            medicine = form.save()
            medicine.save()
            product = form_product.save(commit=False)
            product.medicine = medicine
            product.pharmacy = Pharmacy.objects.get(id=self.kwargs["pharmacy_id"])
            product.save()
            messages.info(self.request, "Product added")
            return HttpResponseRedirect(reverse_lazy("pharmacy", kwargs=self.kwargs))
        else:
            return self.render_to_response(self.get_context_data(form_product=form_product))


class PharmacyAddExistingProductView(CreateView):
    logger.info("Add Existing Product")
    template_name = "pharmacy/add_product.html"
    form_class = ProductForm

    def get_context_data(self, **kwargs):
        context = super(PharmacyAddExistingProductView, self).get_context_data(**kwargs)
        context["medicines"] = Medicine.objects.all()
        return context

    def form_valid(self, form):
        product = form.save(commit=False)
        product.pharmacy = Pharmacy.objects.get(id=self.kwargs["pharmacy_id"])
        product.medicine = Medicine.objects.get(id=self.request.POST.get("medicine_id"))
        product.save()
        messages.info(self.request, "Product added")
        return HttpResponseRedirect(reverse_lazy("pharmacy", kwargs=self.kwargs))


class ProfileView(SuccessMessageMixin, UpdateView):
    logger.info("Profile")
    template_name = "main/profile.html"
    success_message = "Successfully Changed Your Profile"
    success_url = reverse_lazy('main')

    def get_form_class(self):
        if Client.objects.filter(user_id=self.request.user.pk).exists():
            return ClientForm
        else:
            return ApothecaryForm

    def get_object(self):
        if Client.objects.filter(user_id=self.request.user.pk).exists():
            return Client.objects.get(user_id=self.request.user.pk)
        else:
            return Apothecary.objects.get(user_id=self.request.user.pk)


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    logger.info("Change password")
    template_name = 'main/change_password.html'
    form_class = PasswordChangeForm
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('main')
