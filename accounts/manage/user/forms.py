from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth import password_validation
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from accounts import models
from accounts import strings


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'first_name',
                  'last_name', 'email', 'is_active', ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})

class UserPremissionForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['user_permissions']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_permissions'].widget.attrs.update(
            {'class': 'form-control', 'style': 'height: 500px'})
        self.fields['user_permissions'].help_text = strings.USER_PERMISSIONS_FORM_HELP

class UserGroupForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['groups']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['groups'].widget.attrs.update(
            {'class': 'form-control', 'style': 'height: 300px'})
        self.fields['groups'].help_text = strings.USER_GROUPS_FORM_HELP

class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        labels = {
            'user': strings.USER,
            'phone_number': strings.PHONE_NUMBER,
            'avatar': strings.AVATAR,
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
        self.fields['user'].disabled = True
        setting = models.AccountSetting.objects.last()
        max_size = 2
        if setting is not None:
            max_size = setting.avatar_max_file_size
        self.fields['avatar'].help_text = strings.PROFILE_FORM_AVATAR_HELP_TEXT.format(
            max_size)

class SetUserPasswordForm(SetPasswordForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
