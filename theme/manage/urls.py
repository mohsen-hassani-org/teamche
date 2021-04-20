from django.urls import path, include

urlpatterns = [
    path('settings/', include('theme.manage.settings.urls')),
    path('theme/', include('theme.manage.theme.urls')),
    path('menu/', include('theme.manage.menu.urls')),
    path('page/', include('theme.manage.page.urls')),
    path('page/custom/', include('theme.manage.custompage.urls')),
]