from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from accounts.profile import forms
from accounts.models import AccountSetting
from accounts import gvars

@login_required
def profile(request):
    return render(request, 'gentellela/profile.html')

@login_required
def profile_change_password(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            save = form.save()
            user = update_session_auth_hash(request, user)
            return redirect('account_profile')
    else:
        form = PasswordChangeForm(user)
    context = {
        'form': form,
        'form_submit_url_name': 'account_profile_change_password',
        'form_cancel_url_name': 'account_profile',
        'page_title': _('تغییر رمز ورود'),
        'page_subtitle': user.username,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
def profile_edit(request):
    user = request.user
    if request.method == 'POST':
        form1 = forms.UserForm(request.POST, instance=user)
        form2 = forms.ProfileForm(request.POST, request.FILES, instance=user.profile)
        if all([form1.is_valid(), form2.is_valid()]):
            user = form1.save()
            profile = form2.save()
            return redirect('account_profile')
    else:
        form1 = forms.UserForm(instance=user)
        form2 = forms.ProfileForm(instance=user.profile)
    form = [form1, form2]
    context = {
        'forms': form,
        'is_file_form': True,
        'page_title': _('ویرایش اطلاعات کاربری'),
        'page_subtitle': user,
        'form_submit_url_name': 'account_profile_edit',
        'form_cancel_url_name': 'account_profile',
        'form_submit_btn_text': _('ذخیره'),
    }
    return render(request, gvars.GENERIC_MODEL_MULIFORM_TEMPLATE, context)