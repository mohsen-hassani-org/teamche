from django.urls import path, include
from .views import admin, blog_page, post_page, custom_page, start_page, search_page

from django.utils.translation import activate
from django.shortcuts import redirect

def change_lang(request):
    if request.method == 'POST':
        lang = request.POST.get('language')
        activate(lang)
    return redirect('theme_blog_list')

urlpatterns = [
    path('theme/manage/', include('theme.manage.urls')),
    path('blog/', blog_page, name='theme_blog_list'),
    path('blog/<str:slug>/', post_page, name='theme_post'),
    path('search/', search_page, name='theme_search'),
    path('', start_page, name='start'),
    path('admin/', admin, name='admin'),
    path('<str:slug>/', custom_page, name='theme_custom_page'),
    path('i18n/', include('django.conf.urls.i18n')),
]
