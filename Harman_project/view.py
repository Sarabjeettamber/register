from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from Harman_project.settings import *
from django.contrib.auth.models import User

from webpage.models import employees
from webpage.token import account_activation_token


def show(request):
    return HttpResponse("hello world")
def final(request):
    return render(request,"final.html")
def registration(request):
    if request.method == 'POST':
        fn = request.POST['firstname']
        ln = request.POST['lastname']
        em = request.POST['email']
        phone = request.POST['Phone']
        bt = request.POST['r']
        ad = request.POST['address']
        gender = request.POST['gender']
        user = employees(phone=phone, birthday=bt, address=ad, gender=gender, email=em, firstname=fn, lastname=ln)
        user.is_active = False
        user.save()
        current_site = get_current_site(request)

        subject = 'Thanks and Welcome'

        message = render_to_string('activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [em],
            fail_silently=False,
        )

        return redirect('final')
    else:
        return render(request,"registration.html")
