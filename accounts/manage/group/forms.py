from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import SetPasswordForm
from accounts import models
from accounts import strings

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name',]

class GroupPermissionForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['permissions',]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['permissions'].widget.attrs.update({'style': 'height: 500px'})

class UserForm(forms.Form):
    user = forms.ModelChoiceField(queryset=User.objects.all(), label=strings.USER)
    