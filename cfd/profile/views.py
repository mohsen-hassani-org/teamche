import random
from datetime import datetime, timedelta
from re import L
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q, Avg, Count, Min, Max, Sum
from django.db.models.fields import DateField, TimeField
from django.db.models.functions import Concat, Cast
from django.db.models.expressions import Value, F
from django.views.generic import TemplateView
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from cfd.profile.forms import EvaluationForm, SignalEventForm, SignalForm, FillSignalForm, ChooseAnalysisForm,\
                            ClassicAnalysisForm, PTAAnalysisForm, SignalCommentForm,\
                            AppendSignalMistakesForm, SignalEvaluationForm, VolumeProfileAnalysisForm
from cfd.models import Signal, PTAAnalysis, ClassicAnalysis, SignalEvaluation, SignalEvent, Evaluation, VolumeProfileAnalysis
from cfd.gvars import CLASSIC_ANALYSIS_FORM_TEMPLATE, PTA_ANALYSIS_FORM_TEMPLATE, SIGNAL_FORM, SIGNALS, SIGNAL_INFO
from cfd.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST, HTTP403PAGE, GENERIC_MESSAGE, VP_ANALYSIS_FORM_TEMPLATE
from cfd.profile.filters import SignalFilter, ClassicAnalysisFilter, PTAAnalysisFilter
from cfd.profile.utils import classic_analysis_signal_count
from cfd.profile.chart_handler import single_dataset_chart, multi_dataset_chart
from cfd.profile.permissions import team_leader_permission, team_registration_permission
from team.models import Team
from cfd.alerts import DiscordAlert


# @login_required
# def user_summary(request):

#     DATASET = User.objects.all()
#     CHART_TYPE = 'line'
#     X_DATA_TYPE = 'datetime'
#     X_DATA_FIELD = 'date_joined'
#     X_START_RANGE = datetime(year=2021, month=4, day=1)
#     X_END_RANGE = datetime(year=2021, month=6, day=1)
#     X_INTERVAL = 'months'
#     Y_DATA = 'id'
#     OBJECT_FIELD = 'username'
#     OPERATION = Count
#     SUM_RESULTS = True

#     labels = []
#     datasets = []

#     distance = X_START_RANGE - X_END_RANGE
#     interval = getattr(distance, X_INTERVAL)
#     for i in range(int(interval)):
#         date_start = X_START_RANGE + timedelta(i)
#         labels.append(date_start.strftime('%Y-%m-%d'))

#     objects = ''
#     for obj in objects:
#         values = []
#         summ = 0
#         for i in range(int(interval)):
#             date_start = X_START_RANGE + timedelta(i)
#             date_end = date_start + timedelta(days=1)
#             data = Signal.objects.filter(
#                 user=obj, signal_datetime__gt=date_start, signal_datetime__lt=date_end)
#             data = data.aggregate(summ=OPERATION(VALUE))
#             data = data['summ'] if data['summ'] else 0
#             summ = data + summ if SUM_RESULTS else data
#             values.append(summ)
#         datasets.append(
#             {'label': obj, 'data': values, 'color': random_color()})
#     data = {
#         'type': TYPE,
#         'labels': labels,
#         'datasets': datasets,
#     }
#     return render(request, 'test.html', {**data})


# def test(request):
#     # data = single_dataset_chart(qs=Signal.objects.all(), x_data_field='user__username',
#                                 # y_data_field='result_pip', chart_type='bar', operation=Sum, sum_results=False)
#     data = multi_dataset_chart(qs=Signal.objects.all(), x_data_field='user__username',
#       y_data_field='result_pip',dataset_field='asset__name', chart_type='pie', operation=Sum, sum_results=False)
#     return render(request, 'test.html', {**data})


@login_required
def signals_all(request, team_id):
    signals = Signal.signals.get_team_signals(team_id)
    filtered_signals = SignalFilter(request.GET, queryset=signals, team_id=team_id)
    sum_pip = filtered_signals.qs.aggregate(res=Sum('result_pip')).get('res')
    context = {
        'page_title': 'تمامی سیگنال‌ها',
        'items': filtered_signals.qs,
        'fields': ['signal_datetime', 'user', 'asset', 'entry_type', 'result_pip', ],
        'headers': ['زمان', 'کاربر', 'دارایی', 'نوع سیگنال', 'pip', ],
        'filter': filtered_signals,
        'footer_buttons': [{'title': 'بازگشت', 'url_name': 'cfd_profile_signals_month_view', 'url_arg1': team_id}],
        'action_buttons': [
            {
                'title': 'مشاهده جزئیات',
                'url_name': 'cfd_profile_signals_info',
                'arg1_field': 'id',
            },
            {
                'title': 'اشتباهات',
                'url_name': 'cfd_profile_mistakes_append',
                'arg1_field': 'id',
            },
        ],
        'extra_rows': [
            {'title': 'Final PIPs', 'value': sum_pip}
        ],
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
def signals_month(request, team_id):
    if 'month' in request.GET:
        month = request.GET['month']
        month = datetime.strptime(month, '%Y-%m')
    else:
        month = datetime.now().replace(day=1)
    
    signal_type = request.GET.get('signal_type', 'live')
    team = get_object_or_404(Team, id=team_id)
    running_signals = Signal.signals.get_team_running_signals(team_id, signal_type)
    month_signals = Signal.signals.get_month_team_signals(team_id, month)

    data = {
        'all_signals': month_signals,
        'running_signals': running_signals,
        'month': month.strftime('%B'),
        'month_num': month.strftime('%m'),
        'year': month.strftime('%Y'),
        'team': team,
    }
    return render(request, SIGNALS, data)


@login_required
def signal_info(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    user = request.user
    team = signal.team
    team_registration_permission(user, team)
    classic_signal_count = classic_analysis_signal_count(
        signal.classic_analysis.first())
    if request.method == 'POST':
        comment_form = SignalCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            comment.post = signal
            comment.save()
            return redirect('cfd_profile_signals_info', signal_id=signal_id)
    else:
        comment_form = SignalCommentForm()
    now = datetime.now()
    data = {
        'signal': signal,
        'comment_form': comment_form,
        'year': now.year,
        'month': now.strftime('%B'),
        'classic_signals': classic_signal_count,
        'ClassicAnalysis': ClassicAnalysis,
        'PTAAnalysis': PTAAnalysis,
    }
    return render(request, SIGNAL_INFO, data)


@login_required
def view_mistakes(request, team_id):
    pass


@login_required
def signal_result(request):
    pass


@login_required
def append_signal_mistakes(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.method == 'POST':
        form = AppendSignalMistakesForm(request.POST, instance=signal)
        if form.is_valid():
            form.save()
            return redirect('cfd_profile_signals_month_view', team_id=signal.team.id)
    else:
        form = AppendSignalMistakesForm(instance=signal)
    data = {
        'forms': [form],
        'page_title': _('ویرایش اشتباهات سیگنال'),
        'page_subtitle': f'#{signal.id}',
        'form_cancel_url_name': 'cfd_profile_signals_month_view',
        'form_cancel_url_arg1': signal.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def add_signal(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    user_signals = None
    if request.method == 'POST':
        form = SignalForm(request.POST, team=team)
        if form.is_valid():
            open_now = form.cleaned_data['open_now']
            signal = form.save(commit=False)
            signal.user = request.user
            signal.team = team
            if open_now:
                signal.open_signal(signal.entry_point1)
            else:
                signal.save()
            if signal.team.discord_url and signal.signal_type == Signal.SignalType.LIVE:
                DiscordAlert.send_signal_alert(signal)
            messages.success(request, _('سیگنال با موفقیت ایجاد شد.'))
            return redirect('cfd_profile_signals_month_view', team_id=team_id)
    else:
        user_signals = Signal.objects.filter(
            Q(user=request.user) & ~Q(mistakes=None) & ~Q(mistakes=''))[:10]
        form = SignalForm(team=team)
    context = {
        'form': form,
        'user_signals': user_signals,
        'team_id': team_id,
    }
    return render(request, SIGNAL_FORM, context)


@login_required
def view_pta_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    pta = PTAAnalysis.objects.filter(team=team).order_by('-datetime')
    filter_set = PTAAnalysisFilter(request.GET, pta, team_id=team_id)
    for analysis in filter_set.qs:
        analysis.id = analysis.id
        analysis.num = '#{id}'.format(id=analysis.id)
        analysis.user = analysis.user
        analysis.date = analysis.datetime.strftime('%Y %B %d')
        analysis.time = analysis.datetime.strftime('%H:%M:%S')
        analysis.signal_status = analysis.signal or _('ندارد')
        analysis.pip = analysis.signal.result_pip if analysis.signal else '0'
    pips = filter_set.qs.aggregate(pip=Sum('signals__result_pip'))['pip']
    data = {
        'items': filter_set.qs,
        'filter': filter_set,
        'page_title': _('تحلیل‌های PTA'),
        'fields': ['num', 'user', 'signal_status', 'date', 'time', 'pip'],
        'headers': [_('شماره تحلیل'), _('تحلیل‌گر'), _('سیگنال'), _('تاریخ'), _('دقیقه'), _('پیپ نهایی'), ],
        'header_buttons': [
            {
                'title': _('افزودن تحلیل جدید'),
                'url_name': 'cfd_profile_analysis_pta_add',
                'url_arg1': team_id,
            },
        ],
        'action_buttons': [
            {
                'title': _('مشاهده و ویرایش'),
                'url_name': 'cfd_profile_analysis_pta_edit',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'cfd_profile_signals_month_view',
                'url_arg1': team_id,
            },
        ],
        'delete_button_url_name': 'cfd_profile_analysis_pta_delete',
        'extra_rows': [{'title': _('مجموع پیپ'), 'value': pips}]
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
def view_classic_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    classic = ClassicAnalysis.objects.filter(team=team).order_by('-datetime')
    if not request.GET:
        classic = classic.filter(Q(signals__signal_type=Signal.SignalType.LIVE) | Q(signals__isnull=True))
    filter_set = ClassicAnalysisFilter(request.GET, classic, team_id=team_id)
    for analysis in filter_set.qs:
        analysis.num = '#{id}'.format(id=analysis.id)
        analysis.date = analysis.datetime.strftime('%Y %B %d')
        analysis.time = analysis.datetime.strftime('%H:%M:%S')
        signal_type = (
            analysis.signal.get_signal_type_display()
            if analysis.signal
            else ''
        )
        signal_id = analysis.signal.id if analysis.signal else ''
        analysis.signal_status = f'#{signal_id} {analysis.signal} ({signal_type})' or _('ندارد')

    data = {
        'items': filter_set.qs,
        'filter': filter_set,
        'page_title': _('تحلیل‌های Classic'),
        'fields': ['num', 'title', 'user', 'signal_status', 'date', 'time'],
        'headers': [_('شماره تحلیل'), _('عنوان'), _('تحلیل‌گر'), _('سیگنال'), _('تاریخ'), _('دقیقه')],
        'header_buttons': [
            {
                'title': _('افزودن تحلیل جدید'),
                'url_name': 'cfd_profile_analysis_classic_add',
                'url_arg1': team_id,
            },
        ],
        'action_buttons': [
            {
                'title': _('مشاهده و ویرایش'),
                'url_name': 'cfd_profile_analysis_classic_edit',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'cfd_profile_signals_month_view',
                'url_arg1': team_id,
            },
        ],
        'delete_button_url_name': 'cfd_profile_analysis_classic_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
def view_volume_profile_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    vp = VolumeProfileAnalysis.objects.filter(team=team).annotate(
            num=Concat(Value("#"), F("id")),
            date=Cast('datetime', DateField()),
            time=Cast('datetime', TimeField()),
            signal_status=F('signals'),
            pip=Sum('signals__result_pip'),
        ).order_by('-datetime')

    # filter_set = PTAAnalysisFilter(request.GET, pta, team_id=team_id)
    # for analysis in vp:
    #     analysis.signal_status = analysis.signal or _('ندارد')
    #     analysis.pip = analysis.signal.result_pip if analysis.signal else '0'
    pips = vp.aggregate(pip=Sum('signals__result_pip'))['pip']
    
    data = {
        'items': vp,
        # 'filter': filter_set,
        'page_title': _('تحلیل‌های Volume Profile'),
        'fields': ['num', 'title', 'user', 'signal_status', 'date', 'time', 'pip'],
        'headers': [_('شماره تحلیل'), _('عنوان'), _('تحلیل‌گر'), _('سیگنال'), _('تاریخ'), _('دقیقه'), _('پیپ نهایی'), ],
        'header_buttons': [
            {
                'title': _('افزودن تحلیل جدید'),
                'url_name': 'cfd_profile_analysis_vp_add',
                'url_arg1': team_id,
            },
        ],
        'action_buttons': [
            {
                'title': _('مشاهده و ویرایش'),
                'url_name': 'cfd_profile_analysis_vp_edit',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'cfd_profile_signals_month_view',
                'url_arg1': team_id,
            },
        ],
        'delete_button_url_name': 'cfd_profile_analysis_vp_delete',
        'extra_rows': [{'title': _('مجموع پیپ'), 'value': pips}]
    }
    return render(request, GENERIC_MODEL_LIST, data)



@login_required
def pta_analysis_info(request, analysis_id):
    pass


@login_required
def classic_analysis_info(request, analysis_id):
    pass


@login_required
def pta_analysis_edit(request, analysis_id):
    # User cannot edit if analysis added to a signal
    analysis = get_object_or_404(PTAAnalysis, id=analysis_id)
    if request.method == 'POST':
        if analysis.signal:
            data = {
                'message': _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'),
                'message_header': _('توجه!'),
                'message_type': 'danger',
                'message_dismissible': False,
                'back_button': True,
            }
            return render(request, GENERIC_MESSAGE, data)
        form = PTAAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, _('تحلیل با موفقیت ویرایش شد'))
            return redirect('cfd_profile_analysis_pta_view', team_id=analysis.team.id)
    else:
        form = PTAAnalysisForm(instance=analysis)
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل PTA'),
        'page_subtitle': '#{id}'.format(id=analysis_id),
        'form_submit_url_name': 'cfd_profile_analysis_pta_edit',
        'form_submit_url_arg1': analysis_id,
        'form_cancel_url_name': 'cfd_profile_analysis_pta_view',
        'form_cancel_url_arg1': analysis.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def volume_profile_analysis_edit(request, analysis_id):
    # User cannot edit if analysis added to a signal
    analysis = get_object_or_404(VolumeProfileAnalysis, id=analysis_id)
    if request.method == 'POST':
        if analysis.signal:
            messages.error(request, _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'))
            return redirect('cfd_profile_analysis_vp_view', team_id=analysis.team.id)
        form = VolumeProfileAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, _('تحلیل با موفقیت ویرایش شد'))
            return redirect('cfd_profile_analysis_vp_view', team_id=analysis.team.id)
    else:
        form = VolumeProfileAnalysisForm(instance=analysis)
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل Volume Profile'),
        'page_subtitle': '#{id}'.format(id=analysis_id),
        'form_submit_url_name': 'cfd_profile_analysis_vp_edit',
        'form_submit_url_arg1': analysis_id,
        'form_cancel_url_name': 'cfd_profile_analysis_vp_view',
        'form_cancel_url_arg1': analysis.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)



@login_required
def classic_analysis_edit(request, analysis_id):
    # User cannot edit if analysis added to a signal
    analysis = get_object_or_404(ClassicAnalysis, id=analysis_id)
    if request.method == 'POST':
        if analysis.signal:
            messages.error(request, _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'))
            return redirect('cfd_profile_analysis_vp_view', team_id=analysis.team.id)
        form = ClassicAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            messages.success(request, _('تحلیل با موفقیت ویرایش شد'))
            return redirect('cfd_profile_analysis_classic_view', team_id=analysis.team.id)
    else:
        form = ClassicAnalysisForm(instance=analysis)
    data = {
        'form': form,
        'action': 'cfd_profile_analysis_classic_edit',
        'action_arg': analysis.id,
        'team': analysis.team,
    }
    return render(request, CLASSIC_ANALYSIS_FORM_TEMPLATE, data)


@login_required
def pta_analysis_delete(request, analysis_id):
    # User cannot delete if analysis added to a signal
    analysis = get_object_or_404(PTAAnalysis, id=analysis_id)
    if analysis.signal:
        messages.error(request, _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'))
        return redirect('cfd_profile_analysis_pta_view', team_id=analysis.team.id)
    analysis.delete()
    messages.success(request, _('تحلیل با موفقیت حذف شد'))
    return redirect('cfd_profile_analysis_pta_view', team_id=analysis.team.id)


@login_required
def classic_analysis_delete(request, analysis_id):
    # User cannot delete if analysis added to a signal
    analysis = get_object_or_404(ClassicAnalysis, id=analysis_id)
    if analysis.signal:
        messages.error(request, _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'))
        return redirect('cfd_profile_analysis_classic_view', team_id=analysis.team.id)
    analysis.delete()
    messages.success(request, _('تحلیل با موفقیت حذف شد'))
    return redirect('cfd_profile_analysis_classic_view', team_id=analysis.team.id)


@login_required
def volume_profile_analysis_delete(request, analysis_id):
    # User cannot delete if analysis added to a signal
    analysis = get_object_or_404(VolumeProfileAnalysis, id=analysis_id)
    if analysis.signal:
        messages.error(request, _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'))
        return redirect('cfd_profile_analysis_vp_view', team_id=analysis.team.id)
    analysis.delete()
    messages.success(request, _('تحلیل با موفقیت حذف شد'))
    return redirect('cfd_profile_analysis_vp_view', team_id=analysis.team.id)



@login_required
def add_pta_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = PTAAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.team = team
            analysis.save()
            messages.success(request, _('تحلیل با موفقیت ایجاد شد.'))
            return redirect('cfd_profile_analysis_pta_view', team_id=team_id)
    else:
        form = PTAAnalysisForm()
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل PTA'),
        'form_cancel_url_name': 'cfd_profile_analysis_pta_view',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def add_classic_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = ClassicAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.team = team
            analysis.save()
            messages.success(request, _('تحلیل با موفقیت ایجاد شد.'))
            if 'submit_and_signal' in request.POST:
                return redirect('cfd_profile_signals_add', team_id=team_id)
            return redirect('cfd_profile_analysis_classic_view', team_id=team_id)
    else:
        form = ClassicAnalysisForm()
    data = {
        'form': form,
        'action': 'cfd_profile_analysis_classic_add',
        'action_arg': team_id,
        'team': team,
    }
    return render(request, CLASSIC_ANALYSIS_FORM_TEMPLATE, data)

@login_required
def add_volume_profile_analysis(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.method == 'POST':
        form = VolumeProfileAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.team = team
            analysis.save()
            messages.success(request, _('تحلیل با موفقیت ایجاد شد.'))
            return redirect('cfd_profile_analysis_vp_view', team_id=team_id)
    else:
        form = VolumeProfileAnalysisForm()
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل Volume Profile'),
        'form_cancel_url_name': 'cfd_profile_analysis_vp_view',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, VP_ANALYSIS_FORM_TEMPLATE, data)



@login_required
def choose_pta_analysis(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.method == 'POST':
        form = ChooseAnalysisForm(PTAAnalysis, request.POST)
        if form.is_valid():
            analysis = form.cleaned_data.get('analysis', None)
            if analysis != None:
                signal.pta_analysis = analysis
                signal.save()
                return redirect('cfd_profile_signals_info', signal_id=signal_id)
            else:
                form.add_error('analysis', error=_('این فیلد باید پر شود'))
    else:
        form = ChooseAnalysisForm(analysis_type=PTAAnalysis)
    data = {
        'page_title': _('انتخاب تحلیل PTA'),
        'page_subtilte': signal.id,
        'forms': [form],
        'form_cancel_url_name': 'cfd_profile_signals_info',
        'form_cancel_url_arg1': signal.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def choose_classic_analysis(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.method == 'POST':
        form = ChooseAnalysisForm(ClassicAnalysis, request.POST)
        if form.is_valid():
            analysis = form.cleaned_data.get('analysis', None)
            if analysis != None:
                signal.classic_analysis = analysis
                signal.save()
                return redirect('cfd_profile_signals_info', signal_id=signal_id)
            else:
                form.add_error('analysis', error=_('این فیلد باید پر شود'))
    else:
        form = ChooseAnalysisForm(analysis_type=ClassicAnalysis)
    data = {
        'page_title': _('انتخاب تحلیل Classic'),
        'page_subtilte': signal.id,
        'forms': [form],
        'form_cancel_url_name': 'cfd_profile_signals_info',
        'form_cancel_url_arg1': signal.id,
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def remove_classic_analysis(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    signal.classic_analysis = None
    signal.save()
    return redirect('cfd_profile_signals_info', signal_id=signal_id)


@login_required
def remove_pta_analysis(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    signal.pta_analysis = None
    signal.save()
    return redirect('cfd_profile_signals_info', signal_id=signal_id)


@login_required
def fill_signal(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.user != signal.user:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = FillSignalForm(request.POST, instance=signal)
        if form.is_valid():
            current_price = form.cleaned_data.get('current_price', None)
            filled_signal = form.save(commit=False)
            filled_signal.close_signal(current_price)
            messages.success(request, _('سیگنال شما با موفقیت بسته شد'))
            return redirect('cfd_profile_signals_month_view', team_id=signal.team.id)
    else:
        form = FillSignalForm(instance=signal, initial={'result_datetime': datetime.now()})
    context = {
        'forms': [form],
        'page_title': _('فرم پایان معامله'),
        'page_subtitle': _('سیگنال شماره ') + str(signal.id),
        'form_submit_url_name': 'cfd_profile_signals_fill',
        'form_submit_url_arg1': signal.id,
        'form_cancel_url_name': 'cfd_profile_signals_month_view',
        'form_cancel_url_arg1': signal.team.id,
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
    return render(request, GENERIC_MODEL_FORM, context)


# @login_required
# def cancel_signal(request, signal_id):
#     signal = get_object_or_404(Signal, id=signal_id)
#     if request.user != signal.user:
#         return render(request, HTTP403PAGE)
#     signal.status = Signal.SignalStatus.CANCELED
#     signal.canceled_datetime = datetime.now()
#     signal.save()
#     return redirect('cfd_profile_signals_month_view', team_id=signal.team.id)



@login_required
def add_signal_event(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.user != signal.user:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = SignalEventForm(request.POST)
        if form.is_valid():
            event_type = form.cleaned_data.get('event_type', None)
            event_price = form.cleaned_data.get('event_price', None)
            event_desc = form.cleaned_data.get('description ', None)

            if event_type == SignalEvent.EventType.OPEN_SIGNAL:
                signal.open_signal(event_price, event_desc)
            elif event_type == SignalEvent.EventType.CANCEL_SIGNAL:
                signal.cancel_signal(event_price, event_desc)
            else:
                event = form.save(commit=False)
                event.signal = signal
                event.save()
            messages.success(request, _('رویداد جدید با موفقیت به سیگنال اضافه شد'))
            return redirect('cfd_profile_signals_info', signal_id=signal_id)
    else:
        form = SignalEventForm()
    context = {
        'forms': [form],
        'page_title': _('اضافه کردن رویداد به سیگنال'),
        'page_subtitle': _('شماره سیگنال #') + str(signal.id),
        'form_submit_url_name': 'cfd_profile_signal_events_add',
        'form_submit_url_arg1': signal.id,
        'form_cancel_url_name': 'cfd_profile_signals_info',
        'form_cancel_url_arg1': signal.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
def signal_evaluation_list(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.user != signal.team.leader and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    context = {
        'page_title': _('ارزیابی‌های سیگنال'),
        'page_subtitle': signal.id,
        'items': signal.evaluations.all(),
        'fields': ['evaluation', 'weight', 'score'],
        'headers': [_('عنوان'), _('وزن'), _('امتیاز')],
        'header_buttons': [
            {
                'title': _('افزودن ارزیابی جدید'),
                'url_name': 'cfd_profile_signal_evaluations_add',
                'url_arg1': signal_id,
            },{
                'title': _('مدیریت شاخص‌های ارزیابی'),
                'url_name': 'cfd_profile_evaluations_list',
                'url_arg1': signal.team.id,
            },
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'cfd_profile_signal_evaluations_edit',
                'arg1_field': 'id',
            },
        ],
        'footer_buttons': [
            {
                'title': _('بازگشت'),
                'url_name': 'cfd_profile_signals_info',
                'url_arg1': signal_id,
            }
        ],
        'delete_button_url_name': 'cfd_profile_signal_evaluations_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)

@login_required
def signal_evaluation_add(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.user != signal.team.leader and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = SignalEvaluationForm(request.POST)
        if form.is_valid():
            signal_evaluation = form.save(commit=False)
            signal_evaluation.signal = signal
            signal_evaluation.created_by = request.user
            signal_evaluation.save()
            return redirect('cfd_profile_signal_evaluations_list', signal_id=signal_id)
    else:
        form = SignalEvaluationForm()
    context = {
        'forms': [form],
        'page_title': _('افزودن ارزیابی سیگنال'),
        'page_subtitle': f'#{signal.id}',
        'form_submit_url_name': 'cfd_profile_signal_evaluations_add',
        'form_submit_url_arg1': signal_id,
        'form_cancel_url_name': 'cfd_profile_signal_evaluations_list',
        'form_cancel_url_arg1': signal_id,
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
def signal_evaluation_edit(request, signaleval_id):
    signal_evaluation = get_object_or_404(SignalEvaluation, id=signaleval_id)
    if request.user != signal_evaluation.signal.team.leader and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = SignalEvaluationForm(request.POST, instance=signal_evaluation)
        if form.is_valid():
            form.save()
            return redirect('cfd_profile_signal_evaluations_list', signal_id=signal_evaluation.signal.id)
    else:
        form = SignalEvaluationForm(instance=signal_evaluation)
    context = {
        'forms': [form],
        'page_title': _('ویرایش ارزیابی سیگنال'),
        'page_subtitle': f'#{signal_evaluation.id}',
        'form_submit_url_name': 'cfd_profile_signal_evaluations_edit',
        'form_submit_url_arg1': signal_evaluation.id,
        'form_cancel_url_name': 'cfd_profile_signal_evaluations_list',
        'form_cancel_url_arg1': signal_evaluation.signal.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)

@login_required
def signal_evaluation_delete(request, signaleval_id):
    signal_evaluation = get_object_or_404(SignalEvaluation, id=signaleval_id)
    if request.user != signal_evaluation.signal.team.leader and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    signal_evaluation.delete()
    return redirect('cfd_profile_signal_evaluations_list', signal_id=signal_evaluation.signal.id)


@login_required
def evaluation_list(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.users.all() and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    context = {
        'page_title': _('شاخص‌های ارزیابی تیم'),
        'page_subtitle': team,
        'items': Evaluation.objects.filter(team=team),
        'fields': ['name', 'default_weight'],
        'headers': [_('عنوان'), _('وزن')],
        'header_buttons': [
            {
                'title': _('افزودن ارزیابی جدید'),
                'url_name': 'cfd_profile_evaluations_add',
                'url_arg1': team_id,
            }
        ],
        'action_buttons': [
            {
                'title': _('ویرایش'),
                'url_name': 'cfd_profile_evaluations_edit',
                'arg1_field': 'id',
            },
        ],
        'delete_button_url_name': 'cfd_profile_evaluations_delete',
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
def evaluation_add(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if request.user not in team.users.all() and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.team = team
            evaluation.save()
            return redirect('cfd_profile_evaluations_list', team_id=team_id)
    else:
        form = EvaluationForm()
    context = {
        'forms': [form],
        'page_title': _('افزودن شاخص ارزیابی تیم'),
        'page_subtitle': team,
        'form_submit_url_name': 'cfd_profile_evaluations_add',
        'form_submit_url_arg1': team_id,
        'form_cancel_url_name': 'cfd_profile_evaluations_list',
        'form_cancel_url_arg1': team_id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
def evaluation_edit(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if request.user not in evaluation.team.users.all() and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    if request.method == 'POST':
        form = EvaluationForm(request.POST, instance=evaluation)
        if form.is_valid():
            form.save()
            return redirect('cfd_profile_evaluations_list', team_id=evaluation.team.id)
    else:
        form = EvaluationForm(instance=evaluation)
    context = {
        'forms': [form],
        'page_title': _('ویرایش شاخص ارزیابی تیم'),
        'page_subtitle': evaluation,
        'form_submit_url_name': 'cfd_profile_evaluations_edit',
        'form_submit_url_arg1': evaluation_id,
        'form_cancel_url_name': 'cfd_profile_evaluations_list',
        'form_cancel_url_arg1': evaluation.team.id,
    }
    return render(request, GENERIC_MODEL_FORM, context)


@login_required
def evaluation_delete(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    if request.user not in evaluation.team.users.all() and not request.user.is_superuser:
        return render(request, HTTP403PAGE)
    evaluation.delete()
    return redirect('cfd_profile_evaluations_list', team_id=evaluation.team.id)

    
@method_decorator(never_cache, name='dispatch')
class ChooseAnalysis(TemplateView):
    template_name = 'gentelella/choose_analysis.html'

    def get_context_data(self, **kwargs):
        team_id = self.kwargs['team_id']
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('انتخاب آنالیز')
        context['page_subtitle'] = _('انتخاب آنالیز برای تیم')
        context['classic_analysis'] = ClassicAnalysis.objects.filter(team_id=team_id, signals=None).order_by('-id')
        context['classic_analysis_content_type'] = ContentType.objects.get(model=ClassicAnalysis._meta.model_name).id
        context['pta_analysis'] = PTAAnalysis.objects.filter(team_id=team_id, signals=None).order_by('-id')
        context['pta_analysis_content_type'] = ContentType.objects.get(model=PTAAnalysis._meta.model_name).id
        context['vp_analysis'] = VolumeProfileAnalysis.objects.filter(team_id=team_id, signals=None).order_by('-id')
        context['vp_analysis_content_type'] = ContentType.objects.get(model= VolumeProfileAnalysis._meta.model_name).id
        return context