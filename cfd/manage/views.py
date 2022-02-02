from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required, permission_required
from cfd.manage.forms import AssetForm
from cfd.models import Asset
from cfd.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST


@login_required
@permission_required('cfd.asset_view')
def asset_view(request):
    items = Asset.objects.all()
    data = {
        'items': items,
        'page_title': _('مدیریت دارایی‌ها'),
        'fields': ['name',],
        'headers': [_('نام دارایی'), ],
        'header_buttons': [
            {
                'title': _('افزودن'),
                'url_name': 'cfd_manage_asset_add'
            },
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'cfd_manage_asset_edit',
                'arg1_field': 'id'
            },
        ],
        'delete_button_url_name': 'cfd_manage_asset_delete',
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'account_profile',
            }
        ]
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
@permission_required('cfd.asset_add')
def asset_add(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cfd_manage_asset_view')
    else:
        form = AssetForm()
    data = {
        'forms': [form],
        'page_title': _('افزودن دارایی جدید'),
        'form_cancel_url_name': 'cfd_manage_asset_view'
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('cfd.asset_edit')
def asset_edit(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    if request.method == 'POST':
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('cfd_manage_asset_view')
    else:
        form = AssetForm(instance=asset)
    data = {
        'forms': [form],
        'page_title': _('ویرایش دارایی'),
        'page_subtitle': asset.name,
        'form_submit_url_name': 'cfd_manage_asset_edit',
        'form_submit_url_arg1': asset.id,
        'form_cancel_url_name': 'cfd_manage_asset_view'
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('cfd.asset_delete')
def asset_delete(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)
    asset.delete()
    return redirect('cfd_manage_asset_view')