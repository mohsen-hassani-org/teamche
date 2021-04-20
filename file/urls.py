from django.urls import path
from file.manage import views

urlpatterns = [
    path('manage/', views.file_list, name='file_manage_file_list'),
    path('manage/upload/', views.upload_file, name='file_manage_file_upload'),
    path('manage/<int:file_id>/delete/', views.delete_file, name=('file_manage_file_delete')),
    path('manage/<int:file_id>/view/', views.view_file, name=('file_manage_file_view')),
]