import logging
from threading import Thread
from time import time

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import TemplateView, CreateView

from auth.tokens import account_activation_token
from auth.utils import send_request_link
from main.forms import *

logger = logging.getLogger(__name__)


class MyLoginView(LoginView):
    logger.info("Login user")
    form_class = AuthenticationForm
    template_name = "auth/login.html"


class AuthView(TemplateView):
    logger.info("Auth")
    template_name = "auth/auth.html"


class ActivateView(View):
    def get(self, request, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(self.kwargs['uidb64']))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, self.kwargs['token']):
            user.is_active = True
            user.save()
            return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        else:
            return HttpResponse('Activation link is invalid!')


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
        if User.objects.filter(email=form.cleaned_data.get("email")).exists():
            self.form_invalid(form)
        context = self.get_context_data()
        form_client = context['form_client']
        if form_client.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            Thread(target=send_request_link, args=(user, self.request), ).start()

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
        if User.objects.filter(email=form.cleaned_data.get("email")).exists():
            self.form_invalid(form)
        context = self.get_context_data()
        form_apothecary = context['form_apothecary']
        if form_apothecary.is_valid():
            user = form.save()
            user.is_active = False
            user.save()

            Thread(target=send_request_link, args=(user, self.request), ).start()

            apothecary = form_apothecary.save(commit=False)
            apothecary.user = user
            apothecary.save()
            return HttpResponseRedirect(settings.LOGIN_URL)
        else:
            return self.render_to_response(self.get_context_data(form_apothecary=form_apothecary))
