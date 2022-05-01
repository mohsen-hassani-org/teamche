from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse_lazy


class Permissions:
    LOGIN = 'login'
    STAFF = 'staff'
    SUPERUSER = 'superuser'

class PermissionRequireMixin:
    permissions = [Permissions.LOGIN]

    def get(self, *args, **kwargs):
        if not self.has_permission():
            return self.redirect_to_login()
        return super().get(*args, **kwargs)

    def post(self, *args, **kwargs):
        if not self.has_permission():
            return self.redirect_to_login()
        return super().post(*args, **kwargs)
            
    def has_permission(self):
        if self.request.user.is_superuser:
            return True
        if Permissions.LOGIN in self.permissions and not self.request.user.is_authenticated:
            return False
        if Permissions.STAFF in self.permissions and not self.request.user.is_staff:
            return False
        if Permissions.SUPERUSER in self.permissions and not self.request.user.is_superuser:
            return False
        return True
    
    def redirect_to_login(self):
        url = reverse_lazy(settings.LOGIN_URL) + '?next=' + self.request.path
        return redirect(url)
        
        
            

        