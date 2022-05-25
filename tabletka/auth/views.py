import logging
from concurrent.futures import ThreadPoolExecutor

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView

from main.forms import *

logger = logging.getLogger(__name__)


class MyLoginView(LoginView):
    logger.info("Login user")
    form_class = AuthenticationForm
    template_name = "auth/login.html"


class AuthView(TemplateView):
    logger.info("Auth")
    template_name = "auth/auth.html"


class RegisterView(CreateView):
    logger.info("Register client")
    template_name = "auth/register.html"
    form_class = UserForm

    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserForm(self.request.POST)
            context['formC'] = ClientForm(self.request.POST)
        else:
            context['form'] = UserForm()
            context['formC'] = ClientForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formC = context['formC']
        if formC.is_valid():
            self.object = form.save()
            self.object.save()
            client = formC.save(commit=False)
            client.user = self.object
            client.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(formC=formC))


class RegisterApothecaryView(CreateView):
    logger.info("Register apothecary")
    template_name = "auth/register_apothecary.html.html"
    form_class = UserForm

    success_url = reverse_lazy("login")

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserForm(self.request.POST)
            context['formA'] = ApothecaryForm(self.request.POST)
        else:
            context['form'] = UserForm()
            context['formA'] = ApothecaryForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formA = context['formA']
        if formA.is_valid():
            self.object = form.save()
            self.object.save()
            apothecary = formA.save(commit=False)
            apothecary.user = self.object
            apothecary.save()
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data(formA=formA))
