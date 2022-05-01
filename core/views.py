import os
from datetime import datetime
from django import db
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import View, FormView, ListView
from .operations import restore_database
from .forms import BackupForm, RestoreForm
from .permissions import PermissionRequireMixin, Permissions


GENERIC_MODEL_FORM = 'generic_model_multiform.html'
GENERIC_MODEL_LIST = 'generic_model_list.html'


class BackupListView(PermissionRequireMixin, ListView):
    template_name = GENERIC_MODEL_LIST
    permissions = [Permissions.STAFF]

    def get_queryset(self):
        backup_files = []
        path = settings.DBBACKUP_STORAGE_OPTIONS.get('location')
        backup_files_name = os.listdir(path)
        for file in backup_files_name:
            id = ''.join(str(ord(c)) for c in file)
            size = os.path.getsize(os.path.join(path, file)) / 1024 / 1024
            date = os.path.getmtime(os.path.join(path, file))
            date = datetime.fromtimestamp(date)
            backup_files.append({
                'id': id,
                'name': file,
                'size': f'{size:.2f} MB',
                'date': date.strftime('%Y-%m-%d %H:%M:%S')
            })
        return backup_files

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'items': self.get_queryset(),
            'page_title': _('لیست فایل های پشتیبان'),
            'fields': ['name', 'size', 'date'],
            'headers': [_('نام فایل'), _('حجم'), _('تاریخ')],
            'header_buttons': [
                {
                    'title': _('افزودن پشتیبان جدید'),
                    'url_name': 'core:new_backup',
                },
                {
                    'title': _('بازگردانی از فایل'),
                    'url_name': 'core:restore',
                },
            ],
            'action_buttons': [
                {
                    'title': _('دانلود فایل'),
                    'url_name': 'core:download_backup',
                    'arg1_field': 'name',
                },
                {
                    'title': _('بازگردانی فایل'),
                    'url_name': 'core:restore_backup',
                    'arg1_field': 'name',
                },
            ],
            'delete_button_url_name': 'core:delete_backup',
            'delete_item_title_field': 'name',
        })
        return data

class BackupFormView(FormView):
    form_class = BackupForm
    template_name = GENERIC_MODEL_FORM
    success_url = reverse_lazy('core:backups')

    def get(self, request, *args, **kwargs):
        if db.connection.vendor != 'postgresql':
            messages.error(self.request, _(
                'در حال حاضر، امکان تهیه نسخه پشتیبان '
                f'از نوع پایگاه داده {db.connection.vendor} وجود ندارد'
            ))
            return redirect('core:backups')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'forms': [context['form']],
            'page_title': _('تهیه پشتیبان'),
            'form_cancel_url_name': 'core:backups',
        })
        return context

    def form_valid(self, form):
        backup_name = form.save()
        messages.success(self.request, f'پشتیبان گیری با موفقیت انجام شد. نام فایل: {backup_name}')
        return super().form_valid(form)

class DownloadBackupView(PermissionRequireMixin, View):
    def get(self, request, name):
        if not self.has_permission():
            return self.redirect_to_login()
        path = settings.DBBACKUP_STORAGE_OPTIONS.get('location')
        file = open(os.path.join(path, name), 'rb')
        response = HttpResponse(file, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=%s' % name
        return response

class DeleteBackupView(PermissionRequireMixin, View):
    def get(self, request, name):
        if not self.has_permission():
            return self.redirect_to_login()
        path = settings.DBBACKUP_STORAGE_OPTIONS.get('location')
        for file in os.listdir(path):
            id = ''.join(str(ord(c)) for c in file)
            if id == name:
                os.remove(os.path.join(path, file))
                break
        messages.success(
            self.request, f'فایل پشتیبان {name} با موفقیت حذف شد.')
        return redirect('core:backups')

class RestoreFormView(PermissionRequireMixin, FormView):
    permissions = [Permissions.STAFF]
    form_class = RestoreForm
    success_url = reverse_lazy('core:backups')
    template_name = GENERIC_MODEL_FORM
    
    def form_valid(self, form):
        backup_name = form.save()
        restore_database(backup_name)
        messages.success(self.request, 'بازگردانی نسخه پشتیبان با موفقیت انجام شد')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data.update({
            'forms': [data['form']],
            'is_file_form': True,
            'page_title': _('بازگردانی نسخه پشتیبان'),
            'form_cancel_url_name': 'core:backups',
        })
        return data
    
class RestoreBackupView(PermissionRequireMixin, View):
    def get(self, request, name):
        """Get backup name from url and restore it"""
        if not self.has_permission():
            return self.redirect_to_login()
        path = settings.DBBACKUP_STORAGE_OPTIONS.get('location')
        backup_name = os.path.join(path, name)
        if os.path.exists(backup_name):
            restore_database(backup_name)
            messages.success(self.request, f'بازگردانی با موفقیت انجام شد.')
        else:
            messages.error(self.request, f'فایل پشتیبان {name} یافت نشد.')
        return redirect('core:backups')
