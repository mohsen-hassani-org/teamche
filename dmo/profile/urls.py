from django.urls import path
from dmo.profile import views

urlpatterns = [
    path('team/<team_id>/month/', views.all_public_dmos, name="dmo_profile_dmo_view_this_month"),
    path('team/<team_id>/all/', views.view_my_all_dmos, name="dmo_profile_dmo_view_all"),
    path('team/<team_id>/add/', views.add_dmo, name="dmo_profile_dmo_add"),
    path('<int:dmo_id>/edit/', views.edit_dmo, name="dmo_profile_dmo_edit"),
    path('<int:dmo_id>/fill/', views.fill_dmo, name="dmo_profile_dmo_fill"),
    path('<int:dmo_id>/image/', views.dmo_image, name="dmo_profile_dmo_image"),
    path('<int:dmo_id>/delete/', views.delete_dmo, name="dmo_profile_dmo_delete"),
    path('<int:dmo_id>/microactions/', views.view_dmo_microactions, name="dmo_profile_dmo_view_microactions"),
    path('<int:dmo_id>/microactions/add/', views.add_dmo_microaction, name="dmo_profile_dmo_add_microaction"),
    path('microactions/<int:dmo_microaction_id>/edit/', views.edit_dmo_microaction, name="dmo_profile_dmo_edit_microaction"),
    path('microactions/<int:dmo_microaction_id>/delete/', views.delete_dmo_microaction, name="dmo_profile_dmo_delete_microaction"),
    path('<int:dmo_id>/days/', views.dmodays_view, name="dmo_profile_dmodays_view"),
    path('day/<int:dmoday_id>/delete/', views.dmoday_delete, name="dmo_profile_dmoday_delete"),
    path('<int:dmo_id>/view/table/', views.view_dmo_as_table, name="dmo_profile_dmo_view_table"),
    path('team/<int:team_id>/close/', views.close_team_dmos, name='dmo_profile_team_close'),
    path('team/<int:team_id>/settings/', views.dmo_settings, name='dmo_profile_team_settings'),
]