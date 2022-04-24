from django.forms import ModelForm
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from accounts.models import Profile, AccountSetting

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'avatar', 'birth_date', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'] = JalaliDateField(label=_('تاریخ تولد'),
            widget=AdminJalaliDateWidget 
        )
        self.fields['birth_date'].required = False
         
