from django.urls import path
from cfd.manage import views

urlpatterns = [
    path('asset/', views.asset_view, name='cfd_manage_asset_view'),
    path('asset/add/', views.asset_add, name='cfd_manage_asset_add'),
    path('asset/<int:asset_id>/edit/', views.asset_edit, name='cfd_manage_asset_edit'),
    path('asset/<int:asset_id>/delete/', views.asset_delete, name='cfd_manage_asset_delete'),
]