from django.forms import ModelForm
from django.contrib.auth.models import User
from accounts.models import Profile, AccountSetting

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'avatar', ]
