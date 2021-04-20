from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required, permission_required
from accounts import gvars, strings
from accounts.models import Profile
from accounts.manage.user import forms
from django.utils.translation import ugettext as _

@login_required
@permission_required('accounts.view_user', raise_exception=True)
def user_list(request):
    profile_list = Profile.objects.all()
    users_list = []
    for profile in profile_list:
        obj = {}
        obj['id'] = profile.user.id
        obj['username'] = profile.user.username
        obj['firstname'] = profile.user.first_name
        obj['lastname'] = profile.user.last_name
        obj['email'] = profile.user.email
        obj['status'] = strings.USER_ACTIVE if profile.user.is_active else strings.USER_INACTIVE
        users_list.append(obj)

    context = {
        'delete_button_url_name': 'account_manage_user_delete',
        'delete_item_title_field': 'username',
        'page_title': _('لیست کاربران'),
        'items': users_list,
        'headers': [_('نام کاربری'), _('نام'), _('نام خانوادگی'), _('ایمیل'), _('وضعیت'), ],
        'fields': ['username', 'firstname', 'lastname', 'email', 'status', ],
        'header_buttons': [
            {
                'title': _('افزودن کاربر'),
                'url_name': 'account_manage_user_add',
                'fa_icon_name': 'plus',
                # 'class': 'btn-success',
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش کاربر'),
                'url_name': 'account_manage_user_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش پروفایل'),
                'url_name': 'account_manage_profile_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('مجوزها'),
                'url_name': 'account_manage_user_permission_list',
                'arg1_field': 'id',
            },
            {
                'title': _('گروه‌ها'),
                'url_name': 'account_manage_user_group_list',
                'arg1_field': 'id',
            },
            {
                'title': _('تغییر رمز'),
                'url_name': 'account_manage_user_reset_password',
                'arg1_field': 'id',
                'class': 'btn-warning',
            },
        ]
    }
    return render(request, gvars.GENERIC_MODEL_VIEW_TEMPLATE, context)

@login_required
@permission_required('accounts.view_user', raise_exception=True)
def user_view(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return HttpResponse(user)

@login_required
@permission_required('accounts.add_user', raise_exception=True)
def user_add(request):
    if request.method == 'POST':
        form = forms.UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.UserForm()
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_user_add',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'page_title': strings.ADD_USER_FORM_TITLE,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.edit_user', raise_exception=True)
def user_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = forms.UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.UserForm(instance=user)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_user_edit',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': user.id,
        'page_title': strings.EDIT_USER_FORM_TITLE,
        'page_subtitle': user.username,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.edit_user', raise_exception=True)
def profile_edit(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.ProfileForm(instance=profile)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_profile_edit',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': user.id,
        'page_title': strings.EDIT_USER_FORM_TITLE,
        'page_subtitle': user.username,
        'is_file_form': True,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.edit_user_pass', raise_exception=True)
def user_reset_password(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = forms.SetUserPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.SetUserPasswordForm(user)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_user_reset_password',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': user.id,
        'page_title': strings.RESET_USER_PASSWORD,
        'page_subtitle': user.username,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.delete_user', raise_exception=True)
def user_delete(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('account_manage_user_list')

@login_required
@permission_required('accounts.edit_user', raise_exception=True)
def user_deactivate(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    return redirect('account_manage_user_list')

@login_required
@permission_required('accounts.edit_user', raise_exception=True)
def user_activate(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = True
    user.save()
    return redirect('account_manage_user_list')

@login_required
@permission_required('accounts.edit_permission', raise_exception=True)
def user_permissions(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = forms.UserPremissionForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.UserPremissionForm(instance=user)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_user_permission_list',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': user.id,
        'page_title': strings.USER_PERMISSIONS,
        'page_subtitle': user,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)

@login_required
@permission_required('accounts.group_membership', raise_exception=True)
def user_groups(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = forms.UserGroupForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('account_manage_user_list')
    else:
        form = forms.UserGroupForm(instance=user)
    context = {
        'form': form,
        'form_submit_url_name': 'account_manage_user_group_list',
        'form_submit_btn_text': strings.SAVE_FORM,
        'form_cancel_url_name': 'account_manage_user_list',
        'form_cancel_btn_text': strings.CANCEL_FORM,
        'form_submit_url_arg1': user.id,
        'page_title': strings.USER_PERMISSIONS,
        'page_subtitle': user,
    }
    return render(request, gvars.GENERIC_MODEL_FORM_TEMPLATE, context)
