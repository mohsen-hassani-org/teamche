from django.urls import path
from accounts.manage.user import views as user
from accounts.manage.group import views as group
from accounts.manage.settings import views as settings

urlpatterns = [
    path('user/', user.user_list , name='account_manage_user_list'),
    path('user/add/', user.user_add, name='account_manage_user_add'),
    path('user/<int:user_id>/', user.user_view, name='account_manage_user_view'),
    path('user/<int:user_id>/edit/', user.user_edit, name='account_manage_user_edit'),
    path('user/<int:user_id>/delete/', user.user_delete, name='account_manage_user_delete'),
    path('user/<int:user_id>/group/', user.user_groups, name='account_manage_user_group_list'),
    path('user/<int:user_id>/permission/', user.user_permissions, name='account_manage_user_permission_list'),
    path('user/<int:user_id>/reset-password/', user.user_reset_password, name='account_manage_user_reset_password'),

    path('group/', group.group_list , name='account_manage_group_list'),
    path('group/add/', group.group_add, name='account_manage_group_add'),
    path('group/<int:group_id>/edit/', group.group_edit, name='account_manage_group_edit'),
    path('group/<int:group_id>/delete/', group.group_delete, name='account_manage_group_delete'),
    path('group/<int:group_id>/user/', group.group_users, name='account_manage_group_user_list'),
    path('group/<int:group_id>/user/add/', group.group_user_add, name='account_manage_group_user_add'),
    path('group/<int:group_id>/user/<int:user_id>/delete/', group.group_user_delete, name='account_manage_group_user_delete'),
    path('group/<int:group_id>/permission/', group.group_permissions, name='account_manage_group_permission_list'),

    # path('user/<int:user_id>/addresses/add/', views.account_manage_user_address_add, name='account_manage_user_address_add'),
    # path('user/addresses/<int:address_id>/edit/', views.account_manage_user_address_edit, name='account_manage_user_address_edit'),
    # path('user/addresses/<int:address_id>/delete/', views.account_manage_user_address_delete, name='account_manage_user_address_delete'),
    # path('profile/', views.account_manage_profile_detail, name='account_manage_profile_detail'),
    path('profile/<int:user_id>/edit/', user.profile_edit, name='account_manage_profile_edit'),
    # path('profile/change-password/', views.account_manage_profile_change_password, name='account_manage_profile_change_password'),
    # path('permissions/', views.account_manage_permission_list, name='account_manage_permission_list'),
    # path('permissions/user/<int:user_id>/', views.account_manage_permission_user_detail, name='account_manage_permission_user_detail'),
    # path('permissions/user/<int:user_id>/assign/', views.account_manage_permission_user_assign, name='account_manage_permission_user_assign'),
    # path('permissions/user/<int:user_id>/revoke/', views.account_manage_permission_user_revoke, name='account_manage_permission_user_revoke'),
    # path('permissions/user/<int:user_id>/assign/super/', views.account_manage_permission_user_assign_super, name='account_manage_permission_user_assign_super'),
    # path('permissions/user/<int:user_id>/revoke/super/', views.account_manage_permission_user_revoke_super, name='account_manage_permission_user_revoke_super'),
    path('settings/', settings.view_settings, name='account_manage_settings'),
    # path('settings/<int:setting_id>', views.account_manage_setting_edit, name='account_manage_setting_edit'),
]