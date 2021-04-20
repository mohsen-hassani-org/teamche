import ntpath
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_list_or_404, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.translation import ugettext as _
from file.models import File
from file.manage import forms
from file.gvars import GENERIC_MODEL_FORM_TEMPLATE, GENERIC_MODEL_VIEW_TEMPLATE


@login_required
@permission_required('file.view_file', raise_exception=True)
def file_list(request):
    files = File.objects.all()
    items = []
    for file in files:
        size = '{0}MB'.format(round(file.file.size / (1024 * 1024), 2)) if file.file.size > 1024 * 1024 else '{0}KB'.format(round(file.file.size / (1024), 1))
        items.append({
            'id': file.id,
            'name': ntpath.basename(file.file.name),
            'size': size,
            'file': file,
        })
    context = {
        'items': items,
        'page_title': _('فایل‌ها'),
        'fields': ['name', 'size', ],
        'headers': ['فایل', 'حجم', ],
        'delete_button_url_name': 'file_manage_file_delete',
        'header_buttons': [
            {
                'url_name': 'file_manage_file_upload',
                'title': _('بارگذاری فایل جدید'),
            }
        ],
        'action_buttons': [
            {
                'title': _('مشاهده و دانلود'),
                'url_name': 'file_manage_file_view',
                'arg1_field': 'id',
            }
        ]
    }
    return render(request, 'files_list.html', context)


@login_required
@permission_required('file.add_file', raise_exception=True)
def upload_file(request):
    if request.method == 'POST':
        form = forms.FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save()
            return redirect('file_manage_file_list')
    else:
        form = forms.FileForm()
    context = {
        'forms': [form],
        'is_file_form': True,
        'form_submit_url_name': 'file_manage_file_upload',
    }
    return render(request, GENERIC_MODEL_FORM_TEMPLATE, context)


@login_required
@permission_required('file.delete_file', raise_exception=True)
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)    
    file.delete()
    return redirect('file_manage_file_list')


def view_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    return redirect(file.file.url)

