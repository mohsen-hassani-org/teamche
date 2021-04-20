from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from accounts import gvars, strings
from accounts.models import Profile
from accounts.manage.group import forms


@login_required
@permission_required('accounts.view_group')
def group_list(request):
    groups = Group.objects.all()
    group_list = []
    for group in groups:
        obj = {}
        obj['id'] = group.id
        obj['name'] = group.name
        obj['permissions'] = str(group.permissions.count())
        obj['users'] = str(group.user_set.count())
        group_list.append(obj)

    context = {
        'delete_button_url_name': 'account_manage_group_delete',
        'delete_item_title_field': 'name',
        'page_title': _('لیست گروه‌ها'),
        'items': group_list,
        'headers': [_('نام گروه'), _('مجوزها'), _('کاربران'), ],
        'fields': ['name', 'permissions', 'users'],
        'header_buttons': [
            {
                'title': _('افزودن گروه جدید'),
                'url_name': 'account_manage_group_add',
                'fa_icon_name': 'plus',
                # 'class': 'btn-success',
            }
        ],
        'action_buttons': [
            {
                'title': _('لیست کاربران'),
                'url_name': 'account_manage_group_user_list',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش نام گروه'),
                'url_name': 'account_manage_group_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('مجوز‌های گروه'),
                'url_name': 'account_manage_group_permission_list',
                'arg1_field': 'id',
            },
        ]
    }
    return render(request, gvars.GENERIC_MODEL_VIEW_TEMPLATE, context)

@login_required
@permission_required('accounts.add_group')
def group_add(request):
    if request.method == 'POST':
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_manage_group_list')
    else:
        form = forms.GroupForm()
    context = {
        'form': form,
        'page_title': _('افزودن گروه'),
        'form_submit_url_name': 'account_manage_group_add',
        'form_submit_btn_text': _('افزودن'),
        'form_cancel_url_name': 'account_manage_group_list',
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.edit_group')
def group_edit(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = forms.GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('account_manage_group_list')
    else:
        form = forms.GroupForm(instance=group)
    context = {
        'form': form,
        'page_title': _('ویرایش گروه'),
        'form_submit_url_name': 'account_manage_group_edit',
        'form_submit_url_arg1': group_id,
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_group_list',
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.delete_group')
def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    group.delete()
    return redirect('account_manage_group_list')

@login_required
@permission_required('accounts.group_membership')
def group_users(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = group.user_set.all()
    user_list = []
    for user in users:
        obj = {}
        obj['id'] = user.id
        obj['username'] = user.username
        obj['group_id'] = group_id
        user_list.append(obj)
    context = {
        'page_title': _('لیست کاربران گروه'),
        'page_subtitle': group.name,
        'items': user_list,
        'headers': [_('کاربر'), ],
        'fields': ['username', ],
        'header_buttons': [
            {
                'title': _('افزودن کاربر به این گروه'),
                'url_name': 'account_manage_group_user_add',
                'url_arg1': group_id,
                'fa_icon_name': 'plus',
            },
        ],
        'action_buttons': [
            {
                'title': _('حذف کاربر از گروه'),
                'url_name': 'account_manage_group_user_delete',
                'arg1_field': 'id',
                'arg2_field': 'group_id',
                'class': 'btn-danger',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'account_manage_group_list',
            }
        ],
    }
    return render(request, gvars.GENERIC_MODEL_VIEW_TEMPLATE, context)

@login_required
@permission_required('accounts.group_membership')
def group_user_delete(requset, user_id, group_id):
    user = get_object_or_404(User, id=user_id)
    group = get_object_or_404(Group, id=group_id)
    user.groups.remove(group)
    return redirect('account_manage_group_user_list', group_id=group_id)

@login_required
@permission_required('accounts.group_membership')
def group_user_add(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data.get('user')
            group.user_set.add(user)
            return redirect('account_manage_group_user_list', group_id=group_id)
    else:
        form = forms.UserForm()
    context = {
        'form': form,
        'page_title': _('افزودن کاربر به گروه'),
        'page_subtitle': group.name,
        'form_submit_url_name': 'account_manage_group_user_add',
        'form_submit_url_arg1': group_id,
        'form_cancel_url_name': 'account_manage_group_user_list',
        'form_cancel_url_arg1': group_id,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.edit_permission')
def group_permissions(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == 'POST':
        form = forms.GroupPermissionForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('account_manage_group_list')
    else:
        form = forms.GroupPermissionForm(instance=group)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_group_permission_list',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_group_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': group_id,
        'page_title': strings.USER_PERMISSIONS,
        'page_subtitle': group,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

