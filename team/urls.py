from django.urls import path, include

urlpatterns = [
    path('profile/', include('team.profile.urls')),
]