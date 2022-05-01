from django.urls import path
from .views import (
    BackupListView, BackupFormView, RestoreFormView,
    DownloadBackupView, DeleteBackupView, RestoreBackupView
)

app_name = 'core'

urlpatterns = [
    path('backup/', BackupListView.as_view(), name="backups"),
    path('backup/new/', BackupFormView.as_view(), name="new_backup"),
    path('backup/<name>/download/', DownloadBackupView.as_view(), name="download_backup"),
    path('backup/<name>/delete/', DeleteBackupView.as_view(), name="delete_backup"),
    path('restore/', RestoreFormView.as_view(), name="restore"),
    path('restore/<name>/', RestoreBackupView.as_view(), name="restore_backup"),
]