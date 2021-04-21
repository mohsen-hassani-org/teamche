from django.urls import path, include
from django.contrib.auth import views as auth
from accounts.profile import views
from accounts.forms import ForgetPasswordForm, ResetPasswordForm

urlpatterns = [
    path('', views.profile, name='account_profile'),
    path('profile/', views.profile, name='account_profile'),
    path('profile/change-password/', views.profile_change_password, name='account_profile_change_password'),
    path('profile/edit/', views.profile_edit, name='account_profile_edit'),
]
