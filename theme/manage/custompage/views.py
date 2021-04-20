from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from theme.manage.custompage.forms import CustomPageForm
from theme.models import Page, Theme, ThemePage
from theme.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST

@login_required
@permission_required('theme.view_page')
def view_custompages(request):
    pages = Page.objects.filter(page_type='custom')
    context = {
        'page_title': _('صفحات'),
        'items': pages,
        'fields': ['slug', 'theme_page', 'post', 'base',],
        'headers': [_('اسلاگ'), _('قالب صفحه'), _('محتوا'), _('صفحه پایه')],
        'header_buttons': [
            {
                'title': _('افزودن صفحه جدید'),
                'url_name': 'theme_manage_custompage_add',
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'theme_manage_custompage_edit',
                'arg1_field': 'id'
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'theme_manage_theme_list',
            }
        ],
        'delete_button_url_name': 'theme_manage_custompage_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)

@login_required
@permission_required('theme.add_page')
def add_custompage(request):
    if request.method == 'POST':
        form = CustomPageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.page_type = 'custom'
            page.save()
            return redirect('theme_manage_custompage_list')
    else:
        form = CustomPageForm()
    context = {
        'page_title': _('افزودن صفحه جدید'),
        'forms': [form],
        'form_submit_url_name': 'theme_manage_custompage_add',
        'form_cancel_url_name': 'theme_manage_custompage_list',
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
@permission_required('theme.edit_page')
def edit_custompage(request, custompage_id):
    page = get_object_or_404(Page, id=custompage_id)
    if request.method == 'POST':
        form = CustomPageForm(request.POST, instance=page)
        if form.is_valid():
            form.save()
            return redirect('theme_manage_custompage_list')
    else:
        form = CustomPageForm(instance=page)
    context = {
        'page_title': _('ویرایش صفحه'),
        'page_subtitle': page.slug,
        'forms': [form],
        'form_submit_url_name': 'theme_manage_custompage_edit',
        'form_submit_url_arg1': custompage_id,
        'form_cancel_url_name': 'theme_manage_custompage_list',
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
@permission_required('theme.delete_page')
def delete_custompage(request, custompage_id):
    page = get_object_or_404(Page, id=custompage_id)
    page.delete()
    return redirect('theme_manage_custompage_list')

