from django.urls import path 
from theme.manage.theme import views

urlpatterns = [
    path('', views.installed_theme_list, name='theme_manage_theme_list'),    
    path('install/', views.theme_install, name='theme_manage_theme_install'),
    # path('setting/view/', views.view_themesetting, name='theme_manage_themesetting_view'),
    # path('setting/edit/', views.edit_themesetting, name='theme_manage_themesetting_edit'),
    # path('install/', views.theme_install, name='theme_manage_theme_install'),
    path('<int:theme_id>/activate/', views.theme_activate, name='theme_manage_theme_activate'),
    path('<int:theme_id>/deactivate/', views.theme_deactivate, name='theme_manage_theme_deactivate'),
    path('<int:theme_id>/delete/', views.theme_delete, name='theme_manage_theme_delete'),
]