from django.forms import ModelForm
from accounts.models import AccountSetting

class AccountSettingForm(ModelForm):
    class Meta:
        model = AccountSetting
        fields = ('__all__')