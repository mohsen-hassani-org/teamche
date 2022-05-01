import os
import subprocess
from datetime import datetime
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from .operations import backup_database

def now_str():
    return datetime.now().strftime('%Y%m%d_%H%M%S')

class BackupForm(forms.Form):
    backup_name = forms.CharField(label='نام فایل', max_length=255,
                                  initial=now_str)

    def clean_backup_name(self):
        name = self.cleaned_data['backup_name']
        if os.path.exists(os.path.join(settings.DBBACKUP_STORAGE_OPTIONS['location'], name)):
            raise forms.ValidationError('فایل با این نام قبلا ساخته شده است.')
        return name
        
    def save(self):
        name = self.cleaned_data['backup_name']
        name = backup_database(name)
        return name

        

class RestoreForm(forms.Form):
    input_file = forms.FileField(label='فایل پشتیبان')
    
    def clean_input_file(self):
        file = self.cleaned_data['input_file']
        self.__file_path = self._save_file(file)
        proc = subprocess.run(f'file {self.__file_path}', shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = proc.stdout.decode('utf-8')
        if 'PostgreSQL' not in output:
            os.remove(self.__file_path)
            raise forms.ValidationError(_(
                'فایل انتخاب شده یک فایل پشتیبان از پایگاه داده Postgresql نیست.'
            ))

        return file

    def save(self):
        return self.__file_path

    def _save_file(self, file):
        path = os.path.join(settings.DBBACKUP_STORAGE_OPTIONS['location'], file.name)
        with open(path, 'wb') as f:
            for chunk in file.chunks():
                f.write(chunk)
        return path
