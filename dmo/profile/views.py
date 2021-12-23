from datetime import datetime
from django.http.response import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.forms.models import inlineformset_factory
from django.db.models import Q
from django.utils.translation import ugettext as _
from jalali_date import date2jalali
from dmo.alerts import DiscordAlert
from dmo.models import Dmo, DmoDay, Microaction, Setting
from dmo.gvars import DMO_TABLE_TEMPLATE, DMO_CHART_TEMPLATE, ALL_PUBLIC_DMO, DMO_IMAGE_TEMPLATE
from dmo.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST
from dmo.profile.utils import dmo_days_to_data, month_num_to_str, jalali_month_length, dmo_to_table, dmo_last_days
from dmo.profile.forms import DmoForm, MicroactionForm, DmoDayForm, CloseTeamDmoForm, DmoSettingForm
from team.models import Team

@login_required
def view_dmo_as_table(request, dmo_id):
    dmo = get_object_or_404(Dmo, id=dmo_id)
    dmo_data = dmo_days_to_data(dmo)
    table = dmo_to_table(dmo_data)
    context = {
        'dmo': dmo,
        'data': dmo_data,
        'table': table,
    }
    return render(request, DMO_TABLE_TEMPLATE, context)


@login_required
def view_my_all_dmos(request, team_id):
    user = request.user
    team = get_object_or_404(Team, id=team_id, users__in=[user])
    user_dmos = user.dmo_set.filter(team=team)
    dmos = []
    for dmo in user_dmos:
        dmos.append({
            'id': dmo.id,
            'goal': dmo.goal,
            'month': month_num_to_str(dmo.month),
            'year': dmo.year,
        })
    context = {
        'page_title': _('لیست DMOهای من'),
        'page_subtitle': user.get_full_name(),
        'items': dmos,
        'fields': ['goal', 'month', 'year', ],
        'headers': [_('هدف'), _('ماه'), _('سال'), ],
        'action_buttons': [
            {
                'title': _('مشاهده حالت جدولی'),
                'url_name': 'dmo_profile_dmo_view_table',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش'),
                'url_name': 'dmo_profile_dmo_edit',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'dmo_profile_dmo_view_this_month',
                'url_arg1': team_id,
            }
        ],
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
def view_my_this_month_dmos(request):
    user = request.user
    jnow = date2jalali(datetime.now())
    user_dmos = user.dmo_set.filter(month=jnow.month).filter(year=jnow.year)
    dmos = []
    for dmo in user_dmos:
        dmos.append({
            'id': dmo.id,
            'goal': dmo.goal,
            'month': month_num_to_str(dmo.month),
            'year': dmo.year,
        })
    context = {
        'page_title': _('لیست DMOهای من در ماه جاری '),
        'page_subtitle': '{user} - {year}/{month}'.format(user=user.get_full_name(), month=jnow.month, year=jnow.year),
        'items': dmos,
        'fields': ['goal', 'month', 'year', ],
        'headers': [_('هدف'), _('ماه'), _('سال'), ],
        'header_buttons': [
            {
                'title': _('افزودن DMO جدید'),
                'url_name': 'dmo_profile_dmo_add',
            }
        ],
        'action_buttons': [
            {
                'title': _('پرکردن DMO'),
                'url_name': 'dmo_profile_dmo_fill',
                'arg1_field': 'id',
                'class': 'btn-success',
            },
            {
                'title': _('ریزعملکرد روزانه DMO'),
                'url_name': 'dmo_profile_dmodays_view',
                'arg1_field': 'id',
            },
            {
                'title': _('مشاهده حالت جدولی'),
                'url_name': 'dmo_profile_dmo_view_table',
                'arg1_field': 'id',
                'new_tab': True,
            },
            {
                'title': _('ویرایش'),
                'url_name': 'dmo_profile_dmo_edit',
                'arg1_field': 'id',
            },
            {
                'title': _('ویرایش میکرواکشن‌ها'),
                'url_name': 'dmo_profile_dmo_view_microactions',
                'arg1_field': 'id',
            },
        ],
        'delete_button_url_name': 'dmo_profile_dmo_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)

@login_required
def dmo_image(request, dmo_id):
    dmo = get_object_or_404(Dmo, id=dmo_id)
    dmo_data = dmo_days_to_data(dmo)
    table = dmo_to_table(dmo_data)
    context = {
        'dmo': dmo,
        'data': dmo_data,
        'table': table,
    }
    return render(request, DMO_IMAGE_TEMPLATE, context)


@login_required
def add_dmo(request, team_id):
    user = request.user
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, users__in=[request.user])

    if request.method == 'POST':
        form = DmoForm(request.POST)
        if form.is_valid():
            dmo = form.save(commit=False)
            dmo.user = user
            dmo.team = team
            dmo.save()
            if dmo.dmo_type == Dmo.DmoTypes.TEAM and dmo.team.dmo_settings.discord_webhook:
                DiscordAlert.send_new_dmo_alert(dmo)
            return redirect('dmo_profile_dmo_view_this_month', team_id=team_id)
    else:
        form = DmoForm()
    context = {
        'page_title': _('افزودن DMO جدید'),
        'page_subtitle': user.get_full_name(),
        'forms': [form],
        'form_submit_url_name': 'dmo_profile_dmo_add',
        'form_submit_url_arg1': team.id,
        'form_cancel_url_name': 'dmo_profile_dmo_view_this_month',
        'form_cancel_url_arg1': team.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
def edit_dmo(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, id=dmo_id, user=user)
    if request.method == 'POST':
        form = DmoForm(request.POST, instance=dmo)
        if form.is_valid():
            dmo = form.save()
            return redirect('dmo_profile_dmo_view_this_month', team_id=dmo.team.id)
    else:
        form = DmoForm(instance=dmo)
    context = {
        'page_title': _('ویرایش DMO'),
        'page_subtitle': dmo,
        'forms': [form],
        'form_submit_url_name': 'dmo_profile_dmo_edit',
        'form_submit_url_arg1': dmo_id,
        'form_cancel_url_name': 'dmo_profile_dmo_view_this_month',
        'form_cancel_url_arg1': dmo.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
def delete_dmo(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, id=dmo_id, user=user)
    dmo.delete()
    return redirect('dmo_profile_dmo_view_this_month', team_id=dmo.team.id)


@login_required 
def view_dmo_microactions(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, user=user, id=dmo_id)
    microactions = dmo.microactions.all()
    context = {
        'page_title': _('لیست میکرواکشن‌های DMO '),
        'page_subtitle': dmo,
        'items': microactions,
        'fields': ['title', ],
        'headers': [_('عنوان'),],
        'header_buttons': [
            {
                'title': _('افزودن میکرواکشن جدید'),
                'url_name': 'dmo_profile_dmo_add_microaction',
                'url_arg1': dmo_id,
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'dmo_profile_dmo_edit_microaction',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'dmo_profile_dmo_view_this_month',
                'url_arg1': dmo.team.id,
            }
        ],
        'delete_button_url_name': 'dmo_profile_dmo_delete_microaction',
    }
    return render(request, GENERIC_MODEL_LIST, context)

@login_required
def add_dmo_microaction(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, user=user, id=dmo_id)
    if request.method == 'POST':
        form = MicroactionForm(request.POST)
        if form.is_valid():
            microaction = form.save(commit=False)
            microaction.dmo = dmo
            microaction.save()
            return redirect('dmo_profile_dmo_view_microactions', dmo_id=dmo_id)
    else:
        form = MicroactionForm()
    context = {
        'forms': [form],
        'page_title': _('افزودن میکرواکشن DMO'),
        'page_subtitle': dmo,
        'form_submit_url_name': 'dmo_profile_dmo_add_microaction',
        'form_submit_url_arg1': dmo_id,
        'form_cancel_url_name': 'dmo_profile_dmo_view_microactions',
        'form_cancel_url_arg1': dmo_id,
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
def edit_dmo_microaction(request, dmo_microaction_id):
    user = request.user
    microaction = get_object_or_404(Microaction, dmo__user=user, id=dmo_microaction_id)
    if request.method == 'POST':
        form = MicroactionForm(request.POST, instance=microaction)
        if form.is_valid():
            form.save()
            return redirect('dmo_profile_dmo_view_microactions', dmo_id=microaction.dmo.id)
    else:
        form = MicroactionForm(instance=microaction)
    context = {
        'forms': [form],
        'page_title': _('ویرایش میکرواکشن DMO'),
        'page_subtitle': microaction,
        'form_submit_url_name': 'dmo_profile_dmo_edit_microaction',
        'form_submit_url_arg1': dmo_microaction_id,
        'form_cancel_url_name': 'dmo_profile_dmo_view_microactions',
        'form_cancel_url_arg1': microaction.dmo.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
def delete_dmo_microaction(request, dmo_microaction_id):
    user = request.user
    microaction = get_object_or_404(Microaction, dmo__user=user, id=dmo_microaction_id)
    microaction.delete()
    return redirect('dmo_profile_dmo_view_microactions', dmo_id=microaction.dmo.id)

@login_required
def dmodays_view(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, user=user, id=dmo_id)
    dmodays = dmo.days.all()
    items = []
    for dmoday in dmodays:
        items.append({
            'id': dmoday.id,
            'day': _('روز {day}'.format(day=dmoday.day)),
            'done': _('انجام شده') if dmoday.done else _('انجام نشده'),
            'comment': dmoday.comment,
        })
    context = {
        'page_title': _('ریز عملکرد DMO'),
        'page_subtitle': dmo,
        'items': items,
        'fields': ['day', 'done', 'comment', ],
        'headers': [_('روز'), _('وضعیت'), _('توضیحات'), ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'dmo_profile_dmo_view_this_month',
                'url_arg1': dmo.team.id,
            }
        ],
        'delete_button_url_name': 'dmo_profile_dmoday_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)

@login_required
def dmoday_delete(request, dmoday_id):
    user = request.user
    dmoday = get_object_or_404(DmoDay, dmo__user=user, id=dmoday_id)
    if not dmoday.user_locked:
        dmoday.delete()
    return redirect('dmo_profile_dmodays_view', dmo_id=dmoday.dmo.id)

@login_required
def fill_dmo(request, dmo_id):
    user = request.user
    dmo = get_object_or_404(Dmo, user=user, id=dmo_id)
    summary = dmo_last_days(dmo)
    if request.method == 'POST':
        form = DmoDayForm(request.POST)
        if form.is_valid():
            dmoday = form.save(commit=False)
            day = dmoday.day

            # Check for previous dmoday
            prev_day = DmoDay.objects.filter(dmo=dmo, day=day).first()
            if prev_day:
                if prev_day.user_locked:
                    form.add_error('day', _('این روز قفل شده است و امکان تغییر در آن وجود ندارد'))
                else:
                    prev_day.done = True if 'btn_finished' in request.POST else False
                    prev_day.save()
                    return redirect('dmo_profile_dmo_view_this_month', team_id=dmo.team.id)
            else:
                # Save new day data
                dmoday.done = True if 'btn_finished' in request.POST else False
                dmoday.dmo = dmo
                dmoday.save()
                return redirect('dmo_profile_dmo_view_this_month', team_id=dmo.team.id)
    else:
        form = DmoDayForm()
    context = {
        'page_title': _('پرکردن DMO'),
        'page_subtitle': dmo.goal,
        'desc': _('خلاصه ده دوز اخیر نمودار شما:') + '<br/>{sum}'.format(sum=summary),
        'forms': [form],
        'form_submit_url_name': 'dmo_profile_dmo_fill',
        'form_submit_url_arg1': dmo_id,
        'form_cancel_url_name': 'dmo_profile_dmo_view_this_month',
        'form_cancel_url_arg1': dmo.team.id,
        'submit_buttons': [
            {
                'name': 'btn_finished',
                'title': _('انجام شد'),
                'class': 'btn-success',
            },
            {
                'name': 'btn_not_finished',
                'title': _('انجام نشد'),
                'class': 'btn-danger',
            },
        ],
        'extra_head': '''
        <style>
            .dmo_summary {
                border: 1px solid #18252d;
            }
            .dmo_summary tr td {
                border: 1px solid #18252d;
                color: #222;
                height: 15px;
                width: 25px;
                text-align: center;
            }
            .dmo_summary .green {
                background-color: limegreen;
            }
            .dmo_summary .red {
                background-color: indianred;
            }
        </style>
        '''
    }
    return render(request, GENERIC_MODEL_FORM, context)
    # return render(request, 'dmo_fill.html', context)


@login_required
def all_public_dmos(request, team_id):
    user = request.user
    team = get_object_or_404(Team, id=team_id, users__in=[user])

    jnow = date2jalali(datetime.now())
    my_dmos = Dmo.contents.get_my_team_month_dmo(user, team)
    team_dmos = Dmo.contents.get_team_month_dmo(user, team)
    
    for dmo in my_dmos:
        dmo.month_str = month_num_to_str(dmo.month)
        dmo.type_display = dmo.get_dmo_type_display()
        dmo.data = dmo_to_table(dmo_days_to_data(dmo))
        dmo.summary = dmo_last_days(dmo)

    user_seprated_dmos = {}
    for dmo in team_dmos:
        if dmo.user not in user_seprated_dmos.keys():
            user_seprated_dmos[dmo.user] = []
        user_seprated_dmos[dmo.user].append({
            'id': dmo.id,
            'user': dmo.user,
            'goal': dmo.goal,
            'month': month_num_to_str(dmo.month),
            'year': dmo.year,
            'type': dmo.get_dmo_type_display(),
            'data': dmo_to_table(dmo_days_to_data(dmo)),
            'summary': dmo_last_days(dmo),
        })
    items = []
    for user in user_seprated_dmos:
        items.append([user, user_seprated_dmos[user]])
    context = {
        'users': items,
        'my_dmo_set': my_dmos,
        'month': month_num_to_str(jnow.month),
        'year': jnow.year,
        'team': team,
    }
    return render(request, ALL_PUBLIC_DMO, context)


@login_required
def close_team_dmos(request, team_id):
    user = request.user
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = Team.objects.filter(Q(id=team_id), Q(Q(leader=user) | Q(dmo_settings__dmo_manager=user))).first()
        if not team:
            raise Http404()
    if request.method == 'POST':
        form = CloseTeamDmoForm(request.POST)
        if form.is_valid():
            day = form.cleaned_data.get('day')
            if day and day < 31 and day > 0:
                # close all dmos in this day
                dmos = team.dmos.filter(dmo_type=Dmo.DmoTypes.TEAM)
                for dmo in dmos:
                    dmo_day, created = DmoDay.objects.get_or_create(dmo=dmo, day=day, defaults={'done':False, 'user_locked': True})
                return redirect('dmo_profile_dmo_view_this_month', team_id=team_id)
    else:
        form = CloseTeamDmoForm()
    data = {
        'page_title': _('منفی بستن DMO تیمی'),
        'page_subtitle': team.name,
        'forms': [form],
        'form_submit_url_name': 'dmo_profile_team_close',
        'form_submit_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
@permission_required('team.manage_team', raise_exception=True)
def dmo_settings(request, team_id):
    if request.user.is_superuser:
        team = get_object_or_404(Team, id=team_id)
    else:
        team = get_object_or_404(Team, id=team_id, leader=request.user)
    dmo_settings, created = Setting.objects.get_or_create(team=team)
    if request.method == 'POST':
        form = DmoSettingForm(team, request.POST, instance=dmo_settings)
        if form.is_valid():
            form.save()
            return redirect('dmo_profile_dmo_view_this_month', team_id=team_id)
    else:
        form = DmoSettingForm(team, instance=dmo_settings)
    data = {
        'page_title': _('تنظیمات DMO'),
        'page_subtitle': team.name,
        'forms': [form],
    }
    return render(request, GENERIC_MODEL_FORM, data)

