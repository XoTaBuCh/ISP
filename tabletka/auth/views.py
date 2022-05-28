import logging
from concurrent.futures import ThreadPoolExecutor

from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
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

    def get_context_data(self, **kwargs):
        context = super(RegisterView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserForm(self.request.POST)
            context['form_client'] = ClientForm(self.request.POST)
        else:
            context['form'] = UserForm()
            context['form_client'] = ClientForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_client = context['form_client']
        if form_client.is_valid():
            user = form.save()
            user.save()
            client = form_client.save(commit=False)
            client.user = user
            client.save()
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return self.render_to_response(self.get_context_data(form_client=form_client))


class RegisterApothecaryView(CreateView):
    logger.info("Register apothecary")
    template_name = "auth/register_apothecary.html"
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(RegisterApothecaryView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = UserForm(self.request.POST)
            context['form_apothecary'] = ApothecaryForm(self.request.POST)
        else:
            context['form'] = UserForm()
            context['form_apothecary'] = ApothecaryForm()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_apothecary = context['form_apothecary']
        if form_apothecary.is_valid():
            user = form.save()
            user.save()
            apothecary = form_apothecary.save(commit=False)
            apothecary.user = user
            apothecary.save()
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return self.render_to_response(self.get_context_data(form_apothecary=form_apothecary))