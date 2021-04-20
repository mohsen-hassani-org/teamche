from django.urls import path
from theme.manage.menu import views

urlpatterns = [
    path('', views.menu_list, name='theme_manage_menu_list'),
    path('add/', views.menu_add, name='theme_manage_menu_add'),
    path('<int:menu_id>/edit/', views.menu_edit, name='theme_manage_menu_edit'),
    path('<int:menu_id>/delete/', views.menu_delete, name='theme_manage_menu_delete'),
    path('<int:menu_id>/items/', views.item_list, name='theme_manage_menuitem_list'),
    path('<int:menu_id>/items/add/', views.item_add, name='theme_manage_menuitem_add'),
    path('items/<int:menu_item_id>/edit/', views.item_edit, name='theme_manage_menuitem_edit'),
    path('items/<int:menu_item_id>/delete/', views.item_delete, name='theme_manage_menuitem_delete'),
    path('items/<int:menu_item_id>/re-order/', views.reorder_item, name='theme_manage_menuitem_reorder'),
    path('items/<int:menu_item_id>/content/edit/', views.item_contentedit, name='theme_manage_menuitem_contentedit'),
]