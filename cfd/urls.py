from django.urls import path, include

urlpatterns = [
    path('profile/', include('cfd.profile.urls')),
    path('manage/', include('cfd.manage.urls')),
]