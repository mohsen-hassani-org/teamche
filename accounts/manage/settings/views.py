from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from accounts import gvars
from accounts.manage.settings import forms
from accounts.models import AccountSetting

@login_required
@permission_required(['accounts.change_accountsetting', 'accounts.view_accountsetting'], raise_exception=True)
def view_settings(request):
    setting = AccountSetting.objects.last()
    if setting is None:
        setting = AccountSetting()
        setting.save()
    if request.method == 'POST':
        form = forms.AccountSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('account_manage_settings')
    else:
        form = forms.AccountSettingForm(instance=setting)
    context = {
        'forms': [form],
        'page_title': _('تنظیمات حساب کاربری'),
        'form_submit_url_name': 'account_manage_settings',
    }
    return render(request, gvars.GENERIC_MODEL_MULIFORM_TEMPLATE, context )