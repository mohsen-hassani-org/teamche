from django.urls import path
from team.profile.views import *

urlpatterns = [
    path('my/', my_teams, name='team_profile_teams_mine'),
    path('new/', new_team, name='team_profile_teams_new'),
    path('<team_id>/', view_team, name='team_profile_teams_view'),
    path('<team_id>/manage/', manage_team, name='team_profile_teams_manage'),

    path('<team_id>/leave/', leave_team, name='team_profile_teams_leave'),
    path('<team_id>/invite/', invite_to_team, name='team_profile_teams_invite'),
    path('<team_id>/kick/<user_id>/', kick_from_team, name='team_profile_teams_kick'),
    path('<team_id>/promote/<user_id>/', promote_to_leader, name='team_profile_teams_promote'),
    path('invitation/<invitation_id>/accept/', accept_invitation, name='team_profile_invitation_accept'),
    path('invitation/<invitation_id>/reject/', reject_invitation, name='team_profile_invitation_reject'),

    path('<team_id>/votes/', team_votes, name='team_profile_votes_list'),
    path('<team_id>/votes/add/', add_vote, name='team_profile_votes_add'),
    path('votes/<vote_id>/edit/', edit_vote, name='team_profile_votes_edit'),
    path('votes/<vote_id>/delete/', delete_vote, name='team_profile_votes_delete'),
    path('votes/<vote_id>/participate/', participate_vote, name='team_profile_votes_participate'),
    path('votes/participate/<choice_id>/', participate, name='team_profile_participate'),
    path('votes/<vote_id>/result/', vote_result, name='team_profile_votes_result'),
    path('votes/<vote_id>/choices/', vote_choices, name='team_profile_votes_choices'),
    path('votes/<vote_id>/choices/add/', add_vote_choices, name='team_profile_choices_add'),
    path('votes/choices/<choice_id>/edit/', edit_vote_choices, name='team_profile_choices_edit'),
    path('votes/choices/<choice_id>/delete/', delete_vote_choices, name='team_profile_choices_delete'),

    path('<team_id>/meetings/', team_meetings, name='team_profile_meetings_list'),
    path('<team_id>/meetings/add/', add_meeting, name='team_profile_meetings_add'),
    path('meetings/<meeting_id>/edit/', edit_meeting, name='team_profile_meetings_edit'),
    path('meetings/<meeting_id>/delete/', delete_meeting, name='team_profile_meetings_delete'),
    path('meetings/<meeting_id>/proceedings/', view_proceedings, name='team_profile_proceedings_view'),
    path('meetings/<meeting_id>/proceedings/edit/', edit_proceedings, name='team_profile_proceedings_edit'),
    path('meetings/<meeting_id>/proceedings/sign/', sign_proceedings, name='team_profile_proceedings_sign'),

    path('<team_id>/attendances/day/', manage_attendance_day, name='team_profile_attendance_create_today'),
    path('<team_id>/attendances/add/', add_attendance, name='team_profile_attendance_add'),
    path('<team_id>/attendances/list/all/', view_attendance_all, name='team_profile_attendance_view_all'),
    path('<team_id>/attendances/list/today/', view_attendance_today, name='team_profile_attendance_view_today'),
    path('attendances/<attendance_id>/edit/', attendance_edit, name='team_profile_attendance_edit'),
    path('attendances/<attendance_id>/delete/', delete_attendance, name='team_profile_attendance_delete'),
]