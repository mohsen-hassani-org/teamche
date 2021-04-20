from django.contrib import admin
from accounts.models import AccountSetting, Profile

# Register your models here.
admin.site.register(AccountSetting)
admin.site.register(Profile)