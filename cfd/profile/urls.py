from django.urls import path
from cfd.profile import views

urlpatterns = [
    path('signals/all/', views.signals_all, name='cfd_profile_signals_all_view'),
    path('signals/', views.signals_month, name='cfd_profile_signals_month_view'),
    path('signals/add/', views.add_signal, name='cfd_profile_signals_add'),
    path('signals/<signal_id>/analysis/classic/choose/', views.choose_classic_analysis, name='cfd_profile_analysis_classic_choose'),
    path('signals/<signal_id>/analysis/pta/choose/', views.choose_pta_analysis, name='cfd_profile_analysis_pta_choose'),
    path('signals/<signal_id>/analysis/classic/remove/', views.remove_classic_analysis, name='cfd_profile_analysis_classic_remove'),
    path('signals/<signal_id>/analysis/pta/remove/', views.remove_pta_analysis, name='cfd_profile_analysis_pta_remove'),
    path('signals/<signal_id>/', views.signal_info, name='cfd_profile_signals_info'),
    path('signals/<signal_id>/fill/', views.fill_signal, name='cfd_profile_signals_fill'),
    path('signals/<signal_id>/cancel/', views.cancel_signal, name='cfd_profile_signals_cancel'),
    path('signals/<signal_id>/result/', views.signal_result, name='cfd_profile_signals_result'),
    path('signals/<signal_id>/mistakes/append/', views.append_signal_mistakes, name='cfd_profile_mistakes_append'),
    path('signals/mistakes/', views.view_mistakes, name='cfd_profile_signals_mistakes'),
    path('analysis/classic/', views.view_classic_analysis, name='cfd_profile_analysis_classic_view'),
    path('analysis/pta/', views.view_pta_analysis, name='cfd_profile_analysis_pta_view'),
    path('analysis/classic/add/', views.add_classic_analysis, name='cfd_profile_analysis_classic_add'),
    path('analysis/pta/add/', views.add_pta_analysis, name='cfd_profile_analysis_pta_add'),
    path('analysis/classic/<int:analysis_id>/', views.classic_analysis_info, name='cfd_profile_analysis_classic_info'),
    path('analysis/pta/<int:analysis_id>/', views.pta_analysis_info, name='cfd_profile_analysis_pta_info'),
    path('analysis/classic/<int:analysis_id>/edit', views.classic_analysis_edit, name='cfd_profile_analysis_classic_edit'),
    path('analysis/pta/<int:analysis_id>/edit', views.pta_analysis_edit, name='cfd_profile_analysis_pta_edit'),
    path('analysis/classic/<int:analysis_id>/delete', views.classic_analysis_delete, name='cfd_profile_analysis_classic_delete'),
    path('analysis/pta/<int:analysis_id>/delete', views.pta_analysis_delete, name='cfd_profile_analysis_pta_delete'),
]