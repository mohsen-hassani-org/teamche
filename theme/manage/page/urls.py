from django.urls import path
from theme.manage.page import views

urlpatterns = [
    path('<int:theme_id>/', views.theme_pages, name='theme_manage_page_list'),

    path('<int:page_id>/text-variable/', views.page_textvars_list, name='theme_manage_pagetextvars_list'),
    path('text-variable/<int:textvar_id>/content-edit/each/', views.page_textvars_editcontent_each, name='theme_manage_pagetextvars_contentedit_each'),
    path('text-variable/<int:textvar_id>/content-edit/all/', views.page_textvars_editcontent_all, name='theme_manage_pagetextvars_contentedit_all'),

    path('<int:page_id>/image-variable/', views.page_imagevars_list, name='theme_manage_pageimagevars_list'),
    path('image-variable/<int:imagevar_id>/content-edit/each/', views.page_imagevars_editcontent_each, name='theme_manage_pageimagevars_contentedit_each'),
    path('image-variable/<int:imagevar_id>/content-edit/all/', views.page_imagevars_editcontent_all, name='theme_manage_pageimagevars_contentedit_all'),

    path('<int:page_id>/link-variable/', views.page_linkvars_list, name='theme_manage_pagelinkvars_list'),
    path('link-variable/<int:var_id>/content-edit/each/', views.page_linkvars_editcontent_each, name='theme_manage_pagelinkvars_contentedit_each'),
    path('link-variable/<int:var_id>/content-edit/all/', views.page_linkvars_editcontent_all, name='theme_manage_pagelinkvars_contentedit_all'),

    path('<int:page_id>/menu-variable/', views.page_menuvars_list, name='theme_manage_pagemenuvars_list'),
    path('menu-variable/<int:var_id>/content-edit/each/', views.page_menuvars_editcontent_each, name='theme_manage_pagemenuvars_contentedit_each'),
    path('menu-variable/<int:var_id>/content-edit/all/', views.page_menuvars_editcontent_all, name='theme_manage_pagemenuvars_contentedit_all'),

    path('<int:page_id>/cat-variable/', views.page_catvars_list, name='theme_manage_pagecatvars_list'),
    path('cat-variable/<int:var_id>/content-edit/each/', views.page_catvars_editcontent_each, name='theme_manage_pagecatvars_contentedit_each'),
    path('cat-variable/<int:var_id>/content-edit/all/', views.page_catvars_editcontent_all, name='theme_manage_pagecatvars_contentedit_all'),
]