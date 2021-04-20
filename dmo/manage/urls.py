from django.urls import path
from dmo.manage import views

urlpatterns = [
    path('all/', views.view_dmos, name='dmo_manage_dmo_view_all'),
    path('<int:dmo_id>/day/', views.view_dmoday, name='dmo_manage_dmoday_view'),
    path('day/<int:dmoday_id>/delete/', views.dmoday_delete, name='dmo_manage_dmoday_delete'),

]