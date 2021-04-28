import pytz
from datetime import datetime
from django.conf import settings
from django.http import HttpResponse, Http404
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import login_required, permission_required
from team.models import *
from team.profile.forms import *
from team.gvars import *

@login_required
def my_teams(request):
    teams = request.user.teams.filter()
    items = []
    for team in teams:
        items.append({
            'id': team.id,
            'name': team.name,
            'leader': team.leader if team.leader != request.user else _('شما'),
            'users': team.users.count(),
            'invitations': str(team.invitations.filter(action=TeamInvitation.ActionTypes.NO_ACTION).count()),
            'can_manage': '' if team.leader == request.user else 'hide',
            'can_leave': 'hide' if team.leader == request.user else '',
        })
    invitations = request.user.team_invitations.filter(action=TeamInvitation.ActionTypes.NO_ACTION)
    data = {
        'items': items,
        'my_invitations': invitations,
        'action_buttons': [
            {
                'title': _('مشاهده'),
                'url_name': 'team_profile_teams_view',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش'),
                'url_name': 'team_profile_teams_manage',
                'arg1_field': 'id',
                'class_from_field': 'can_manage',
            },
            {
                'title': _('ارسال دعوت‌نامه'),
                'url_name': 'team_profile_teams_invite',
                'arg1_field': 'id',
                'class_from_field': 'can_manage',
            },
            {
                'title': _('حضور و غیاب'),
                'url_name': 'team_profile_attendance_view_today',
                'arg1_field': 'id',
            },
            {
                'title': _('جلسات'),
                'url_name': 'team_profile_meetings_list',
                'arg1_field': 'id',
            },
            {
                'title': _('نظرسنجی‌ها'),
                'url_name': 'team_profile_votes_list',
                'arg1_field': 'id',
            },
            {
                'title': _('ترک تیم'),
                'url_name': 'team_profile_teams_leave',
                'arg1_field': 'id',
                'class': 'btn-danger',
                'class_from_field': 'can_leave',
            },
        ]
    }
    return render(request, MY_TEAMS_TEMPLATE, data)


@login_required
def new_team(request):
    if request.method == 'POST':
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.leader = request.user
            team.save()
            team.users.add(request.user) # Add user to team users
            # Add manage permission to user
            permission = Permission.objects.get(codename='manage_team')
            request.user.user_permissions.add(permission)
            # Get user again for cache problem
            return redirect('team_profile_teams_mine')
    else:
        form = TeamForm()
    data = {
        'page_title': _('ایجاد تیم جدید'),
        'forms': [form],
        'form_cancel_url_name': 'team_profile_teams_mine',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def view_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    users = team.users.all()
    items = []
    for user in users:
        items.append({
            'id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'team_id': team.id,
            'role': _('رهبر') if user==team.leader else _('عضو'),
            'is_leader': '' if request.user==team.leader else 'hide', 
            # 'has_perm': '' if request.user=team.leader else 'hide',
        })
    data = {
        'page_title': _('مشاهده گروه'),
        'page_subtitle': team.name,
        'items': items,
        'fields': ['username', 'first_name', 'last_name', 'role', ],
        'headers': [_('نام کاربری'), _('نام'), _('نام خانوادگی'), _('نقش')],
        'action_buttons': [
            {
                'title': _('ارتقا به رهبر'),
                'url_name': 'team_profile_teams_promote',
                'arg1_field': 'team_id',
                'arg2_field': 'id',
                'class': 'btn-success',
                'class_from_field': 'is_leader',
            },
            {
                'title': _('بیرون انداختن از گروه'),
                'url_name': 'team_profile_teams_kick',
                'arg1_field': 'team_id',
                'arg2_field': 'id',
                'class': 'btn-danger',
                'class_from_field': 'is_leader',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'team_profile_teams_mine',
            }
        ],
        
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def manage_team(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            return redirect('team_profile_teams_mine')
    else:
        form = TeamForm(instance=team)
    data = {
        'page_title': _('ویرایش تیم'),
        'page_subtitle': team.name,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_teams_mine',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def invite_to_team(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        form = TeamInvitationForm(request.user, request.POST)
        if form.is_valid():
            users = form.cleaned_data.get('users')
            bulk = [TeamInvitation(team=team, user=user, request_datetime=datetime.now()) for user in users]
            TeamInvitation.objects.bulk_create(bulk)
            return redirect('team_profile_teams_mine')
    else:
        form = TeamInvitationForm(user=request.user)
    data = {
        'page_title': _('دعوت به تیم'),
        'page_subtitle': team.name,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_teams_mine',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def promote_to_leader(request, team_id, user_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    new_leader = get_object_or_404(User, id=user_id, id__in=team.users.all())
    old_leader = request.user
    team.leader = new_leader
    team.save()
    # revoke manage permission form old_leader and assign to new_leader
    permission = Permission.objects.get(codename='manage_team')
    new_leader.user_permissions.add(permission)
    old_leader.user_permissions.remove(permission)
    return redirect('team_profile_teams_mine')


@login_required
@permission_required('team.manage_team', raise_exception=True)
def kick_from_team(request, team_id, user_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    user = get_object_or_404(User, id=user_id, id__in=team.users.all())
    if user == team.leader:
        data = {
            'message': _('امکان ترک تیم توسط رهبر گروه وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    else:
        user.teams.remove(team)
    return redirect('team_profile_teams_mine')


@login_required
def leave_team(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    if request.user == team.leader:
        data = {
            'message': _('امکان ترک تیم توسط رهبر گروه وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    else:
        request.user.teams.remove(team)
    return redirect('team_profile_teams_mine')


@login_required
def accept_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id, user=request.user, action=TeamInvitation.ActionTypes.NO_ACTION)
    team = invitation.team
    team.users.add(request.user)
    invitation.action = TeamInvitation.ActionTypes.ACCEPT
    invitation.action_datetime = datetime.now()
    invitation.save()
    return redirect('team_profile_teams_view', team_id=team.id)

@login_required
def reject_invitation(request, invitation_id):
    invitation = get_object_or_404(TeamInvitation, id=invitation_id, user=request.user, action=TeamInvitation.ActionTypes.NO_ACTION)
    team = invitation.team
    invitation.action = TeamInvitation.ActionTypes.REJECT
    invitation.action_datetime = datetime.now()
    invitation.save()
    return redirect('team_profile_teams_mine')

@login_required
def team_votes(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    votes = Vote.objects.filter(team=team)
    items = []
    for vote in votes:
        items.append({
            'id': vote.id,
            'title': vote.title,
            'due': vote.due_datetime,
            'vote_type': vote.get_vote_type_display(),
        })
    data = {
        'page_title': _('نظرسنجی‌های تیم'),
        'page_subtitle': team.name,
        'items': items,
        'fields': ['title', 'due', 'vote_type', ],
        'headers': [_('عنوان'), _('مهلت'), _('نوع نظرسنجی'), ],
        'header_buttons': [{'title': _('ایجاد نظرسنجی'), 'url_name': 'team_profile_votes_add',
                            'url_arg1': team_id, 'class': 'btn-success', 'fa_icon_name': 'plus'}],
        'footer_buttons': [{'title': _('بازگشت'), 'url_name': 'team_profile_teams_mine'}],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'team_profile_votes_edit',
                'arg1_field': 'id'  
            },
            {
                'title': _('گزینه‌ها'),
                'url_name': 'team_profile_votes_choices',
                'arg1_field': 'id'  
            },
            {
                'title': _('نتایج'),
                'url_name': 'team_profile_votes_result',
                'arg1_field': 'id'  
            },
            {
                'title': _('شرکت در نظرسنجی'),
                'url_name': 'team_profile_votes_participate',
                'arg1_field': 'id'  
            },
        ],
        'delete_button_url_name': 'team_profile_votes_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)
    

@login_required
@permission_required('team.manage_team', raise_exception=True)
def add_vote(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.team = team
            vote.save()
    else:
        form = VoteForm()
    data = {
        'page_title': _('ایجاد نظرسنجی'),
        'page_subtitle': team.name,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_votes_list',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)



@login_required
@permission_required('team.manage_team', raise_exception=True)
def edit_vote(request, vote_id):
    if request.user.is_superuser:
        vote = get_object_or_404(Vote, id=vote_id)
    else:
        vote = get_object_or_404(Vote, id=vote_id, team_leader=request.user)
    team = vote.team
    # if anyone participated in the vote, it cannot be deleted
    votes = UserVote.objects.filter(user_choice__vote=vote)
    if votes:
        data = {
            'message': _('در این نظرسنجی افرادی شرکت کرده‌اند و امکان حذف آن وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    if request.method == 'POST':
        form = VoteForm(request.POST, instance=vote)
        if form.is_valid():
            vote = form.save(commit=False)
            vote.team = team
            vote.save()
            return redirect('team_profile_votes_list', team_id=team.id)
    else:
        form = VoteForm(instance=vote)
    data = {
        'page_title': _('ویرایش نظرسنجی'),
        'page_subtitle': vote.title,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_votes_list',
        'form_cancel_url_arg1': team.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)




@login_required
@permission_required('team.manage_team', raise_exception=True)
def delete_vote(request, vote_id):
    if request.user.is_superuser:
        vote = get_object_or_404(Vote, id=vote_id)
    else:
        vote = get_object_or_404(Vote, id=vote_id, team_leader=request.user)
    team = vote.team
    # if anyone participated in the vote, it cannot be deleted
    votes = UserVote.objects.filter(user_choice__vote=vote)
    if votes:
        data = {
            'message': _('در این نظرسنجی افرادی شرکت کرده‌اند و امکان حذف آن وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    else:
        vote.delete()
    return redirect('team_profile_votes_list', team_id=team.id)


@login_required
def participate_vote(request, vote_id):
    vote = get_object_or_404(Vote, id=vote_id, team__users__in=[request.user])
    team = vote.team
    now = datetime.now()
    vote_date = vote.due_datetime

    # Convert vote_date and now to local timezone
    settings_time_zone = pytz.timezone(settings.TIME_ZONE)
    vote_date = vote_date.astimezone(settings_time_zone)
    now = now.astimezone(settings_time_zone)

    if vote_date < now:
        data = {
            'message': _('مهلت شرکت در این نظرسنجی تمام شده است'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    # Praticipate in vote
    return render(request,  PARTICIPATE_TEMPLATE, {'vote': vote})

@login_required
def participate(request, choice_id):
    choice = get_object_or_404(VoteChoice, id=choice_id, vote__team__users__in=[request.user])
    vote = choice.vote
    team = vote.team
    vote_date = vote.due_datetime
    user_choice = UserVote.objects.filter(user=request.user, user_choice__vote=vote).first()
    if user_choice:
        data = {
            'message': _('شما قبلا در این نظرسنجی شرکت کرده‌اید'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
 
    utc=pytz.UTC
    now = utc.localize(datetime.now())
    if vote_date > now:
        data = {
            'message': _('مهلت شرکت در این نظرسنجی تمام شده است'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    user_vote = UserVote(user=request.user, user_choice=choice, voted_date=now)
    user_vote.save()
    return redirect('team_profile_votes_result', vote_id=vote.id)

 


@login_required
def vote_result(request, vote_id):
    vote = get_object_or_404(Vote, id=vote_id, team__users__in=[request.user])
    team = vote.team
    vote_type = vote.vote_type
    vote_choices = vote.choices.all()
    items = []
    for vote_choice in vote_choices:
        tmp_object = {}
        tmp_object['id'] = vote_choice.id,
        tmp_object['title'] = vote_choice.choice
        tmp_object['votes'] = str(vote_choice.user_votes.count())
        voters = [(vote.user.get_full_name() or vote.user.username) for vote in vote_choice.user_votes.all()]
        tmp_object['voters'] = ', '.join(voters) if vote_type == Vote.VoteTypes.PUBLIC else _('نامشخص')
        items.append(tmp_object)
    data = {
        'page_title': _('مشاهده نتایج'),
        'page_subtitle': vote.title,
        'items': items,
        'fields': ['title', 'votes', 'voters', ],
        'headers': [_('عنوان'), _('آرا'), _('رای دهندگان'), ],
        'footer_buttons': [{'title': _('بازگشت'), 'url_name': 'team_profile_votes_list', 'url_arg1': team.id}],
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def vote_choices(request, vote_id):
    if request.user.is_superuser:
        vote = get_object_or_404(Vote, id=vote_id)
    else:
        vote = get_object_or_404(Vote, id=vote_id, team_leader=request.user)
    team = vote.team
    choices = vote.choices.all()
    data = {
        'items': choices,
        'fields': ['choice', ],
        'headers': [_('گزینه'), ],
        'page_title': _('گزینه‌های نظرسنجی'),
        'page_subtitle': vote.title,
        'header_buttons': [{'title': _('افزودن گزینه جدید'), 'url_name': 'team_profile_choices_add', 'url_arg1': vote_id}],
        'footer_buttons': [{'title': _('بازگشت'), 'url_name': 'team_profile_votes_list', 'url_arg1': team.id}],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'team_profile_choices_edit',
                'arg1_field': 'id',
            },
        ],
        'delete_button_url_name': 'team_profile_choices_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def add_vote_choices(request, vote_id):
    if request.user.is_superuser:
        vote = get_object_or_404(Vote, id=vote_id)
    else:
        vote = get_object_or_404(Vote, id=vote_id, team_leader=request.user)
    team = vote.team
    # if anyone participated in the vote, it cannot be deleted
    votes = UserVote.objects.filter(user_choice__vote=vote)
    if votes:
        data = {
            'message': _('در این نظرسنجی افرادی شرکت کرده‌اند و امکان تغییر در آن وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    if request.method == 'POST':
        form = VoteChoiceForm(request.POST)
        if form.is_valid():
            vote_choice = form.save(commit=False)
            vote_choice.vote = vote
            vote_choice.save()
            return redirect('team_profile_votes_choices', vote_id)
    else:
        form = VoteChoiceForm()
    data = {
        'page_title': _('ایجاد گزینه جدید'),
        'page_subtitle': vote.title,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_votes_choices',
        'form_cancel_url_arg1': vote_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def edit_vote_choices(request, choice_id):
    if request.user.is_superuser:
        choice = get_object_or_404(VoteChoice, id=choice_id)
    else:
        choice = get_object_or_404(VoteChoice, id=choice_id, vote__team__leader=request.user)
    vote = choice.vote
    # if anyone participated in the vote, it cannot be deleted
    votes = UserVote.objects.filter(user_choice__vote=vote)
    if votes:
        data = {
            'message': _('در این نظرسنجی افرادی شرکت کرده‌اند و امکان تغییر در آن وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    if request.method == 'POST':
        form = VoteChoiceForm(request.POST, instance=choice)
        if form.is_valid():
            vote_choice = form.save(commit=False)
            vote_choice.vote = vote
            vote_choice.save()
            return redirect('team_profile_votes_choices', choice.vote.id)
    else:
        form = VoteChoiceForm(instance=choice)
    data = {
        'page_title': _('ویرایش گزینه'),
        'page_subtitle': choice.choice,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_votes_choices',
        'form_cancel_url_arg1': choice.vote.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def delete_vote_choices(request, choice_id):
    if request.user.is_superuser:
        choice = get_object_or_404(VoteChoice, id=choice_id)
    else:
        choice = get_object_or_404(VoteChoice, id=choice_id, vote__team__leader=request.user)
    vote = choice.vote
    # if anyone participated in the vote, it cannot be deleted
    votes = UserVote.objects.filter(user_choice__vote=vote)
    if votes:
        data = {
            'message': _('در این نظرسنجی افرادی شرکت کرده‌اند و امکان تغییر در آن وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    choice.delete()
    return redirect('team_profile_votes_choices', choice.vote.id)






@login_required
def team_meetings(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    meetings = team.meetings.all()
    items = []
    for meeting in meetings:
        items.append({
            'id': meeting.id,
            'title': meeting.title,
            'datetime': meeting.datetime,
            'signs': str(meeting.signatures.count()),
            'proceedings': _('تنظیم شده') if meeting.proceedings else _('ندارد'),
        })
    data = {
        'page_title': _('جلسات گروه'),
        'page_subtitle': team.name,
        'items': items,
        'fields': ['title', 'signs', 'datetime', 'proceedings', ],
        'headers': [_('عنوان'), _('تعداد امضا'), _('تاریخ'), _('خلاصه صورت‌جلسه'), ],
        'header_buttons': [{'title': _('ایجاد جلسه جدید'), 'url_name': 'team_profile_meetings_add', 'url_arg1': team.id}],
        'footer_buttons': [{'title': _('بازگشت'), 'url_name': 'team_profile_teams_mine'}],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'team_profile_meetings_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('صورت‌جلسه'),
                'url_name': 'team_profile_proceedings_view',
                'arg1_field': 'id',
            },
        ],
        'delete_button_url_name': 'team_profile_meetings_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def add_meeting(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.team = team
            meeting.save()
            return redirect('team_profile_meetings_list', team_id=team_id)
    else:
        form = MeetingForm()
    data = {
        'page_title': _('افزودن جلسه'),
        'page_subtitle': team.name,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_meetings_list',
        'form_cancel_url_arg1': team.id,
        'extra_head': '''
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
            <script src="/static/vendors/bootstrap/dist/js/bootstrap.js"></script>
            <style>
                .datetimepicker {
                    right: auto;
                }
            </style>
        ''',
    }
    return render(request, GENERIC_MODEL_FORM, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def edit_meeting(request, meeting_id):
    if request.user.is_superuser:
        meeting = get_object_or_404(Meeting, id=meeting_id)
    else:
        meeting = get_object_or_404(Meeting, id=meeting_id, team__leader=request.user)
    if meeting.signatures.count() > 0:
        data = {
            'message': 'صورت‌جلسه این جلسه توسط حداقل یک نفر امضا شده است و امکان ویرایش آن وجود ندارد',
            'message_type': 'danger',
            'message_dismissable': False,
            'message_header': _('اخطار'),
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            meeting = form.save()
            return redirect('team_profile_meetings_list', team_id=meeting.team.id)
    else:
        form = MeetingForm(instance=meeting)
    data = {
        'page_title': _('ویرایش جلسه'),
        'page_subtitle': meeting.title,
        'forms': [form],
        'form_cancel_url_name': 'team_profile_meetings_list',
        'form_cancel_url_arg1': meeting.team.id,
        'extra_head': '''
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.8.3/jquery.min.js"></script>
            <script src="/static/vendors/bootstrap/dist/js/bootstrap.js"></script>
            <style>
                .datetimepicker {
                    right: auto;
                }
            </style>
        '''
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def delete_meeting(request, meeting_id):
    if request.user.is_superuser:
        meeting = get_object_or_404(Meeting, id=meeting_id)
    else:
        meeting = get_object_or_404(Meeting, id=meeting_id, team__leader=request.user)
    if meeting.signatures.count() > 0:
        data = {
            'message': 'صورت‌جلسه این جلسه توسط حداقل یک نفر امضا شده است و امکان حذف آن وجود ندارد',
            'message_type': 'danger',
            'message_dismissable': False,
            'message_header': _('اخطار'),
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    meeting.delete()
    return redirect('team_profile_meetings_list', team_id=meeting.team.id)

@login_required
def view_proceedings(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, team__users__in=[request.user])
    data = {
        'meeting': meeting,
    }
    return render(request, PROCEEDINGS_TEMPLATE, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def edit_proceedings(request, meeting_id):
    if request.user.is_superuser:
        meeting = get_object_or_404(Meeting, id=meeting_id)
    else:
        meeting = get_object_or_404(Meeting, id=meeting_id, team__leader=request.user)
    if meeting.signatures.count() > 0:
        data = {
            'message': 'صورت‌جلسه این جلسه توسط حداقل یک نفر امضا شده است و امکان ویرایش آن وجود ندارد',
            'message_type': 'danger',
            'message_dismissable': False,
            'message_header': _('اخطار'),
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    if request.method == 'POST':
        form = ProceddingsForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('team_profile_proceedings_view', meeting_id=meeting_id)
    else:
        form = ProceddingsForm(instance=meeting)
    data = {
        'page_title': _('صورت‌جلسه ') + meeting.team.name,
        'page_subtitle': '{title} - {date}'.format(title=meeting.title, date=meeting.datetime),
        'form': form,
        'form_cancel_url_name': 'team_profile_meetings_list',
        'form_cancel_url_arg1': meeting.team.id,
    }
    return render(request, GENERIC_TEXT_EDITOR, data)


@login_required
def sign_proceedings(request, meeting_id):
    meeting = get_object_or_404(Meeting, id=meeting_id, team__users__in=[request.user])
    user_signs = meeting.signatures.filter(user=request.user, meeting=meeting).first()
    if not user_signs:
        sign = MeetingSigature(user=request.user, meeting=meeting, sign_date=datetime.now())
        sign.save()
        meeting.signatures.add(sign)
    return redirect('team_profile_proceedings_view', meeting_id=meeting_id)





















@login_required
def view_attendance_today(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    now = datetime.now()
    date = datetime(year=now.year, month=now.month, day=now.day)
    attendances = Attendance.objects.filter(date=date, team=team)
    items = []
    for att in attendances:
        items.append({
            'id': att.id,
            'user': att.user,
            'type': att.get_attendance_type_display(),
            'hours': '{0} ساعت'.format(att.leave_hours) if att.leave_hours else '',
        })
    data = {
        'page_title': _('لیست حضور و غیاب'),
        'page_subtitle': team.name,
        'items': items,
        'fields': ['user', 'type', 'hours',],
        'headers': [_('کاربر'), _('نوع حضور'), _('ساعت مرخصی')],
        'header_buttons': [
            {
                'title': _('ایجاد لیست امروز'),
                'class': 'btn-success',
                'url_name': 'team_profile_attendance_create_today',
                'url_arg1': team_id,
            },
            {
                'title': _('افزودن تکی'),
                'url_name': 'team_profile_attendance_add',
                'url_arg1': team_id,
            },
            {
                'title': _('مشاهده همه'),
                'url_name': 'team_profile_attendance_view_all',
                'url_arg1': team_id,
            },
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'team_profile_attendance_edit',
                'arg1_field': 'id',
            }
        ],
        'footer_buttons': [{'title': _('بازگشت'), 'url_name': 'team_profile_teams_mine'}],
        'delete_button_url_name': 'team_profile_attendance_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)

@login_required
def view_attendance_all(request, team_id):
    team = get_object_or_404(Team, id=team_id, users__in=[request.user])
    filter_form = AttendanceSearchForm(team)
    attendances = Attendance.objects.filter(team=team)
    if request.method == 'GET':
        filter_form = AttendanceSearchForm(team, request.GET)
        if filter_form.is_valid():
            user = filter_form.cleaned_data.get('user')
            att_type = filter_form.cleaned_data.get('att_type')
            sdate = filter_form.cleaned_data.get('sdate')
            edate = filter_form.cleaned_data.get('edate')
            attendances = attendances.filter(user=user) if user else attendances
            attendances = attendances.filter(attendance_type=att_type) if att_type else attendances
            attendances = attendances.filter(date__gte=sdate) if sdate else attendances
            attendances = attendances.filter(date__lte=edate) if edate else attendances

    items = []
    for att in attendances:
        items.append({
            'id': att.id,
            'user': att.user,
            'date': att.date,
            'type': att.get_attendance_type_display(),
            'hours': '{0} ساعت'.format(att.leave_hours) if att.leave_hours else '',
        })
    data = {
        'page_title': _('لیست حضور و غیاب'),
        'page_subtitle': team.name,
        'items': items,
        'fields': ['user', 'date', 'type', 'hours', ],
        'headers': [_('کاربر'),_('تاریخ'), _('نوع حضور'), _('ساعت مرخصی')],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'team_profile_attendance_view_today',
                'url_arg1': team_id,
            }
        ],
        'filter_form': filter_form,
    }
    return render(request, GENERIC_MODEL_LIST, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def manage_attendance_day(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    now = datetime.now()
    if Attendance.objects.filter(date=now, team=team).count() > 0:
        data = {
            'message': _('برای امروز قبلا لیست را ایجاد کرده‌اید'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    users = team.users.all()
    AttendanceFormSet = formset_factory(AttendanceForm, extra=0)
    if request.method == 'POST':
        formset = AttendanceFormSet(request.POST, form_kwargs={'team': team})
        if formset.is_valid():
            for form in formset:
                attendance = form.save(commit=False)
                attendance.team = team
                attendance.save()
            return redirect('team_profile_attendance_view_today', team_id=team_id)
    else:
        inital_data = []
        for user in users:
            inital_data.append({'user': user, 'attendance_type': Attendance.AttendanceType.ABSENT})
        formset = AttendanceFormSet(initial=inital_data, form_kwargs={'team': team})
    data = {
        'page_title': _('ایجاد لیست امروز'),
        'page_subtitle': now.strftime('%Y/%m/%d'), 
        'formset': formset,
        'extra_head': '''
            <style>
                .form-group ul {
                    list-style: none; padding: 7px 10px 0px 0px;}
                .form-group ul li {
                    float: right; padding: 0px 15px; }
            </style>
            ''',
        'form_cancel_url_name': 'team_profile_attendance_view_today',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def add_attendance(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    if request.method == 'POST':
        form = AttendanceFormWithDate(team, request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            attendance.team = team
            attendance.save()
            return redirect('team_profile_attendance_view_today', team_id=team_id)
    else:
        form = AttendanceFormWithDate(team)
    data = {
        'page_title': _('فرم افزودن حضور و غیاب'),
        'forms': [form],
        'extra_head': '''
            <style>
                .form-group ul {
                    list-style: none; padding: 7px 10px 0px 0px;}
                .form-group ul li {
                    float: right; padding: 0px 15px; }
            </style>
            ''',
        'form_cancel_url_name': 'team_profile_attendance_view_today',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def attendance_edit(request, attendance_id):
    if request.user.is_superuser:
        attendance = get_object_or_404(Attendance, id=attendance_id)
    else:
        attendance = get_object_or_404(Attendance, id=attendance_id, team__leader=request.user)
    if request.method == 'POST':
        form = AttendanceForm(attendance.team, request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('team_profile_attendance_view_today', team_id=attendance.team.id)
    else:
        form = AttendanceForm(attendance.team, instance=attendance)
    data = {
        'page_title': _('فرم ویرایش حضور و غیاب'),
        'page_subtitle': attendance.user,
        'forms': [form],
        'extra_head': '''
            <style>
                .form-group ul {
                    list-style: none; padding: 7px 10px 0px 0px;}
                .form-group ul li {
                    float: right; padding: 0px 15px; }
            </style>
            ''',
        'form_cancel_url_name': 'team_profile_attendance_view_today',
        'form_cancel_url_arg1': attendance.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)

@login_required
@permission_required('team.manage_team', raise_exception=True)
def delete_attendance(request, attendance_id, team_id):
    if request.user.is_superuser:
        attendance = get_object_or_404(Attendance, id=attendance_id)
    else:
        attendance = get_object_or_404(Attendance, id=attendance_id, team_leader=request.user)
    attendance = get_object_or_404(Attendance, id=attendance_id, team=team)
    attendance.delete()
    return redirect('team_profile_attendance_view_today', attendance_id=attendance_id)


