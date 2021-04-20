from django.urls import path, include
from django.contrib.auth import views as auth
from accounts.auth import views
from accounts.forms import ForgetPasswordForm, ResetPasswordForm

urlpatterns = [
    path('login/', auth.LoginView.as_view(template_name='gentellela/login.html'),
         name='account_login'),
    path('logout/', auth.LogoutView.as_view(), name='account_logout'),
    path('register/', views.register, name='account_register'),
    path('register/complete/', views.register_succeed,
         name='account_register_succeed'),
    path('forgot-password/', auth.PasswordResetView.as_view(template_name='gentellela/forgot_password.html',
                                                            form_class=ForgetPasswordForm, success_url='sent/'),
                                                            name='account_forgot_password'),
    path('forgot-password/sent/', views.forgot_password_email_sent,
         name='forgot_password_email_sent'),
    path('forgot-password/new-password/<str:uidb64>/<str:token>/', auth.PasswordResetConfirmView.as_view(
        template_name='gentellela/reset_password.html', form_class=ResetPasswordForm, 
        success_url='/accounts/forgot-password/new-password/done/'), name='password_reset_confirm'),
    path('forgot-password/new-password/done/',
         views.reset_password_done, name='password_reset_done'),
    # path('logout/', ,name='account_logout'),
]
