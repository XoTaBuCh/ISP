from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from auth.tokens import account_activation_token


def send_request_link(user, request):
    current_site = get_current_site(request)
    subject = 'Activate your tabletkas account.'
    message = render_to_string('auth/acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    return send_mail(subject, message, 'tabletka.lab4', [user.email], fail_silently=False)

