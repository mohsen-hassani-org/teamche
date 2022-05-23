from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
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
    birth_date = request.user.profile.birth_date
    age_treshold = None
    if birth_date is not None:
        date1 = birth_date- timedelta(days=birth_date.weekday())
        date2 = datetime.now().date() - timedelta(days=datetime.now().date().weekday())
        age_treshold = (date2 - date1).days / 7
    context = {
        'YEARS': list(range(70)),
        'WEEKS': list(range(1, 53)),
        'AGE_TRESHOLD': age_treshold,
        'todo_list': {
            'date': datetime.now().date(),
        }
    }
    return render(request, 'gentellela/profile.html', context)

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
        user_form = forms.UserForm(request.POST, instance=user)
        profile_form = forms.ProfileForm(request.POST, request.FILES, instance=user.profile)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save()
            profile = profile_form.save()
            messages.success(request, _('اطلاعات با موفقیت بروزرسانی شد.'))
            return redirect('account_profile')
    else:
        user_form = forms.UserForm(instance=user)
        profile_form = forms.ProfileForm(instance=user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'is_file_form': True,
        'years': list(range(1201, 1470)),
        'page_title': _('ویرایش اطلاعات کاربری'),
        'page_subtitle': user,
        'form_submit_url_name': 'account_profile_edit',
        'form_cancel_url_name': 'account_profile',
        'form_submit_btn_text': _('ذخیره'),
        'persian_date_fields': ['birth_date'],
        
    }
    return render(request, gvars.PROFILE_FORM_TEMPLATE, context)