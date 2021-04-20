from django.http import Http404
from django.views.i18n import set_language
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from accounts import models
from accounts import forms
from accounts import gvars


def register(request):
    setting = models.AccountSetting.objects.last()
    can_register = True
    if setting is not None:
        can_register = setting.user_can_register
    if not can_register:
        raise Http404()
    if request.method == 'POST':
        form = forms.UserPassAuthForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data['email']
            user.save()
            return redirect('account_register_succeed')
    else:
        form = forms.UserPassAuthForm()
    return render(request, gvars.REGISTER_TEMPLATE, {'form': form})


def register_succeed(request):
    return render(request, gvars.REGISTER_CONFIMATION_TEMPLATE)


def forgot_password_email_sent(request):
    return render(request, gvars.FORGOT_PASSWORD_EMAIL_SENT_TEMPLATE)


def reset_password_done(request):
    return render(request, gvars.RESET_PASSWORD_DONE_TEMPLATE)
