from django.urls import path
from theme.manage.custompage import views

urlpatterns = [
    path('', views.view_custompages, name='theme_manage_custompage_list'),
    path('add/', views.add_custompage, name='theme_manage_custompage_add'),
    path('<int:custompage_id>/edit/', views.edit_custompage, name='theme_manage_custompage_edit'),
    path('<int:custompage_id>/delete/', views.delete_custompage, name='theme_manage_custompage_delete'),
]