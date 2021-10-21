from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from accounts import strings

CSS_CLASS = 'form-control'

class UserPassAuthForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': strings.USERNAME_FORM_LABEL, 'class': CSS_CLASS, 'style': 'text-transform:lowercase;'}), label=strings.USERNAME_FORM_LABEL)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': strings.EMAIL_FORM_LABEL, 'class': CSS_CLASS}), label=strings.EMAIL_FORM_LABEL)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': strings.PASSWORD_FORM_LABEL, 'class': CSS_CLASS}), label=strings.PASSWORD_FORM_LABEL)
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': strings.PASSWORD_CONFIRM_FORM_LABEL, 'class': CSS_CLASS}), label=strings.PASSWORD_CONFIRM_FORM_LABEL)

class ForgetPasswordForm(PasswordResetForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': strings.EMAIL_FORM_LABEL, 'class': CSS_CLASS}), label=strings.EMAIL_FORM_LABEL)

class ResetPasswordForm(SetPasswordForm):
    pass