from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from theme.models import SiteSetting
from theme.manage.settings.forms import SiteSettingForm
from theme.gvars import GENERIC_MODEL_INFO, GENERIC_MODEL_FORM


@login_required
@permission_required('theme.view_sitesetting')
def view_sitesetting(request):
    setting = SiteSetting.objects.get_or_create()[0]
    context = {
        'item': setting,
        'meta': setting._meta,
        'page_title': 'تنظیمات سایت',
        'header_buttons': [{
            'title': _('ویرایش تنظیمات'),
            'url_name': 'theme_manage_setting_edit',
        }],
        'fields': ['site_title', 'site_subtitle', 'home_page','primary_light_color', 'primary_bold_color', 'primary_dark_color', 'accend_light_color', 'accend_bold_color', 'accend_dark_color', ],
    }
    return render(request, GENERIC_MODEL_INFO, context)


@login_required
@permission_required('theme.edit_sitesetting')
def edit_sitesetting(request):
    setting = SiteSetting.objects.get_or_create()[0]
    if request.method == 'POST':
        form = SiteSettingForm(request.POST, instance=setting)
        if form.is_valid():
            form.save()
            return redirect('theme_manage_setting_view')
    else:
        form = SiteSettingForm(instance=setting)
    context = {
        'forms': [form],
        'page_title': _('ویرایش تنظیمات سایت'),
        'form_submit_url_name': 'theme_manage_setting_edit',
        'form_cancel_url_name': 'theme_manage_setting_view',
    }
    return render(request, GENERIC_MODEL_FORM, context)

