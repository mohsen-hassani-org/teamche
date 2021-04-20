import os
import shutil
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from django.http import Http404, HttpResponse
from theme.models import Theme, Page
from theme.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST
from theme.manage.theme import forms
from theme.manage.theme.theme_installer import install_theme


@login_required
@permission_required('theme.view_theme')
def installed_theme_list(request):
    themes = Theme.objects.all()
    context = {
        'themes': themes,
    }
    return render(request, 'system/gentellela/themes.html', context)

@login_required
@permission_required('theme.add_theme')
def theme_install(requset):
    if requset.method == 'POST':
        form = forms.InstallZipThemeForm(requset.POST, requset.FILES)
        if form.is_valid():
            errors = install_theme(form.cleaned_data.get('zip_file'))
            if not errors:
                return redirect('theme_manage_theme_list')
            form.add_error('zip_file', _(errors))
    else:
        form = forms.InstallZipThemeForm()
    context = {
        'forms': [form],
        'form_submit_url_name': 'theme_manage_theme_install',
        'is_file_form': True,
    }
    return render(requset, GENERIC_MODEL_FORM, context)

@login_required
@permission_required('theme.edit_theme')
def theme_activate(request, theme_id):
    active_themes = Theme.objects.filter(is_active=True)
    for active_theme in active_themes:
        active_theme.is_active = False
        active_theme.save()
    theme = get_object_or_404(Theme, id=theme_id)
    theme.is_active = True
    theme.save()
    return redirect('theme_manage_theme_list')

@login_required
@permission_required('theme.edit_theme')
def theme_deactivate(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    theme.is_active = False
    theme.save()
    return redirect('theme_manage_theme_list')

@login_required
@permission_required('theme.delete_theme')
def theme_delete(request, theme_id):
    theme = get_object_or_404(Theme, id=theme_id)
    cwd = os.getcwd()

    # delete theme static folder
    shutil.rmtree(
        '{cwd}/static/theme/themes/{theme}'.format(cwd=cwd, theme=theme.name))

    # delete theme folder
    shutil.rmtree(
        '{cwd}/theme/templates/themes/{theme}'.format(cwd=cwd, theme=theme.name))

    # delete pages with this theme
    pages = Page.objects.filter(theme_page__theme=theme)
    pages.delete()

    # delete theme itself
    theme.delete()

    return redirect('theme_manage_theme_list')


# @login_required
# @permission_required('theme.view_themesetting')
# def view_themesetting(request):
#     setting = ThemeSetting.objects.get_or_create()[0]
#     context = {
#         'item': setting,
#         'meta': setting._meta,
#         'page_title': 'تنظیمات قالب',
#         'header_buttons': [{
#             'title': _('ویرایش تنظیمات'),
#             'url_name': 'theme_manage_themesetting_edit',
#         }],
#         'fields': ['primary_light_color', 'primary_bold_color', 'primary_dark_color', 'accend_light_color', 'accend_bold_color', 'accend_dark_color',]
#     }
#     return render(request, GENERIC_MODEL_INFO, context)

# @login_required
# @permission_required('theme.edit_themesetting')
# def edit_themesetting(request):
#     setting = ThemeSetting.objects.get_or_create()[0]
#     if request.method == 'POST':
#         form = ThemeSettingForm(request.POST, instance=setting)
#         if form.is_valid():
#             form.save()
#             return redirect('theme_manage_themesetting_view')
#     else:
#         form = ThemeSettingForm(instance=setting)
#     context = {
#         'forms': [form],
#         'page_title': _('ویرایش تنظیمات قالب'),
#         'form_submit_url_name': 'theme_manage_themesetting_edit',
#         'form_cancel_url_name': 'theme_manage_themesetting_view',
#     }
#     return render(request, GENERIC_MODEL_FORM, context)


