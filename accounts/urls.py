from django.urls import path, include
from django.contrib.auth import views as auth
from accounts.forms import ForgetPasswordForm, ResetPasswordForm

urlpatterns = [
    path('manage/', include('accounts.manage.urls')),
    path('', include('accounts.auth.urls')),
    path('', include('accounts.profile.urls')),
]