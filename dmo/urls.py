from django.urls import path, include

urlpatterns = [
    path('profile/', include('dmo.profile.urls')),
    path('manage/', include('dmo.manage.urls')),
]