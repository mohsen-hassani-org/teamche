from django.apps import AppConfig
from django.utils.translation import ugettext_lazy

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = ugettext_lazy('مدیریت حساب‌ها')