from django.forms import ModelForm
from django.forms import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
from accounts.models import Profile, AccountSetting

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].disabled = True

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
        self.fields['phone_number'].widget.attrs.update({'placeholder': _('09xxxxxxxxx')})

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and phone_number.startswith('09'):
            return phone_number
        raise ValidationError(_('شماره تماس باید با 09 شروع شود.'))
