"""stonestore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
# import locale
# locale.setlocale(locale.LC_ALL, "fa_IR")

urlpatterns = [
    path('d/admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='account_profile')),
    path('account/', include('accounts.urls')),
    path('admin/', include('accounts.urls')),
    path('dmo/', include('dmo.urls')),
    path('cfd/', include('cfd.urls')),
    path('team/', include('team.urls')),
    path('file/', include('file.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
