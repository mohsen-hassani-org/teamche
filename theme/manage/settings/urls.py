from django.urls import path
from theme.manage.settings import views

urlpatterns = [
    path('view/', views.view_sitesetting, name='theme_manage_setting_view'),
    path('edit/', views.edit_sitesetting, name='theme_manage_setting_edit'),
]