from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required
from cfd.profile.forms import SignalForm, FillSignalForm, ChooseAnalysisForm
from cfd.profile.forms import ClassicAnalysisForm, PTAAnalysisForm, SignalCommentForm, AppendSignalMistakesForm
from cfd.models import Signal, PTAAnalysis, ClassicAnalysis
from cfd.gvars import CLASSIC_ANALYSIS_FORM_TEMPLATE, PTA_ANALYSIS_FORM_TEMPLATE, SIGNAL_FORM, SIGNALS, SIGNAL_INFO
from cfd.gvars import GENERIC_MODEL_FORM, GENERIC_MODEL_LIST, HTTP403PAGE, GENERIC_MESSAGE
from cfd.profile.utils import classic_analysis_signal_count


@login_required
def signals_all(request):
    signals = Signal.objects.all()
    context = {
        'items': signals,
        'headers': ['زمان', 'کاربر', 'دارایی', 'نوع سیگنال', ],
        'fields': ['signal_datetime', 'user', 'asset', 'entry_type', ],
    }
    return render(request, GENERIC_MODEL_LIST, context)


@login_required
def signals_month(request):
    if 'month' in request.GET:
        month = request.GET['month']
        month = datetime.strptime(month, '%Y-%m')
        try:
            next_month = month.replace(month=month.month+1)
        except ValueError:
            if month.month == 12:
                next_month = month.replace(year=month.year + 1, month=1)
            else:
                next_month = month
    else:
        month = datetime.now().replace(day=1)
    running_signals = Signal.objects.filter(status=Signal.SignalStatus.RUNNING)
    month_signals = Signal.objects.filter(~Q(status=Signal.SignalStatus.RUNNING) & Q(
        result_datetime__gt=month) & Q(result_datetime__lt=next_month))
    data = {
        'all_signals': month_signals,
        'running_signals': running_signals,
        'month': month.strftime('%B'),
        'month_num': month.strftime('%m'),
        'year': month.strftime('%Y'),
    }
    return render(request, SIGNALS, data)


@login_required
def signal_info(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    classic_signal_count = classic_analysis_signal_count(
        signal.classic_analysis)
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
    }
    return render(request, SIGNAL_INFO, data)


@login_required
def view_mistakes(request):
    pass


@login_required
def signal_report(request):
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
            return redirect('cfd_profile_signals_month_view')
    else:
        form = AppendSignalMistakesForm(instance=signal)
    data = {
        'forms': [form],
        'page_title': _('ویرایش اشتباهات سیگنال'),
        'page_subtitle': f'#{signal.id}',
        'form_cancel_url_name': 'cfd_profile_signals_month_view',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def add_signal(request):
    user_signals = None
    if request.method == 'POST':
        form = SignalForm(request.POST)
        if form.is_valid():
            signal = form.save(commit=False)
            signal.user = request.user
            signal.save()
            return redirect('cfd_profile_signals_month_view')
    else:
        user_signals = Signal.objects.filter(
            Q(user=request.user) & ~Q(mistakes=None) & ~Q(mistakes=''))[:10]
        form = SignalForm()
    context = {
        'form': form,
        'user_signals': user_signals,
    }
    return render(request, SIGNAL_FORM, context)


@login_required
def view_pta_analysis(request):
    pta = PTAAnalysis.objects.all().order_by('datetime')
    items = []
    for analysis in pta:
        items.append({
            'id': analysis.id,
            'num': '#{id}'.format(id=analysis.id),
            'user': analysis.user,
            'date': analysis.datetime.strftime('%Y %B %d'),
            'time': analysis.datetime.strftime('%H:%M:%S'),
            'signal': analysis.signal if hasattr(analysis, 'signal') else _('ندارد')
        })
    data = {
        'items': items,
        'page_title': _('تحلیل‌های PTA'),
        'fields': ['num', 'user', 'signal', 'date', 'time'],
        'headers': [_('شماره تحلیل'), _('تحلیل‌گر'), _('سیگنال'), _('تاریخ'), _('دقیقه')],
        'header_buttons': [
            {
                'title': _('افزودن تحلیل جدید'),
                'url_name': 'cfd_profile_analysis_pta_add',
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
            },
        ],
        'delete_button_url_name': 'cfd_profile_analysis_pta_delete',
    }
    return render(request, GENERIC_MODEL_LIST, data)


@login_required
def view_classic_analysis(request):
    classic = ClassicAnalysis.objects.all().order_by('datetime')
    items = []
    for analysis in classic:
        items.append({
            'id': analysis.id,
            'num': '#{id}'.format(id=analysis.id),
            'title': analysis.title,
            'user': analysis.user,
            'date': analysis.datetime.strftime('%Y %B %d'),
            'time': analysis.datetime.strftime('%H:%M:%S'),
            'signal': analysis.signal if hasattr(analysis, 'signal') else _('ندارد')
        })
    data = {
        'items': items,
        'page_title': _('تحلیل‌های Classic'),
        'fields': ['num', 'title', 'user', 'signal', 'date', 'time'],
        'headers': [_('شماره تحلیل'), _('عنوان'), _('تحلیل‌گر'), _('سیگنال'), _('تاریخ'), _('دقیقه')],
        'header_buttons': [
            {
                'title': _('افزودن تحلیل جدید'),
                'url_name': 'cfd_profile_analysis_classic_add',
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
            },
        ],
        'delete_button_url_name': 'cfd_profile_analysis_classic_delete',
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
        if hasattr(analysis, 'signal'):
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
            return redirect('cfd_profile_analysis_pta_view')
    else:
        form = PTAAnalysisForm(instance=analysis)
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل PTA'),
        'page_subtitle': '#{id}'.format(id=analysis_id),
        'form_submit_url_name': 'cfd_profile_analysis_pta_edit',
        'form_submit_url_arg1': analysis_id,
        'form_cancel_url_name': 'cfd_profile_analysis_pta_view',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def classic_analysis_edit(request, analysis_id):
    # User cannot edit if analysis added to a signal
    analysis = get_object_or_404(ClassicAnalysis, id=analysis_id)
    if request.method == 'POST':
        if hasattr(analysis, 'signal'):
            data = {
                'message': _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'),
                'message_header': _('توجه!'),
                'message_type': 'danger',
                'message_dismissible': False,
                'back_button': True,
            }
            return render(request, GENERIC_MESSAGE, data)
        form = ClassicAnalysisForm(request.POST, instance=analysis)
        if form.is_valid():
            form.save()
            return redirect('cfd_profile_analysis_classic_view')
    else:
        form = ClassicAnalysisForm(instance=analysis)
    data = {
        'form': form,
        'action': 'cfd_profile_analysis_classic_edit',
        'action_arg': analysis.id,
    }
    return render(request, CLASSIC_ANALYSIS_FORM_TEMPLATE, data)


@login_required
def pta_analysis_delete(request, analysis_id):
    # User cannot delete if analysis added to a signal
    analysis = get_object_or_404(PTAAnalysis, id=analysis_id)
    if hasattr(analysis, 'signal'):
        data = {
            'message': _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    analysis.delete()
    return redirect('cfd_profile_analysis_pta_view')


@login_required
def classic_analysis_delete(request, analysis_id):
    # User cannot delete if analysis added to a signal
    analysis = get_object_or_404(ClassicAnalysis, id=analysis_id)
    if hasattr(analysis, 'signal'):
        data = {
            'message': _('امکان حدف یا ویرایش تحلیل‌هایی که دارای سیگنال می‌باشند وجود ندارد'),
            'message_header': _('توجه!'),
            'message_type': 'danger',
            'message_dismissible': False,
            'back_button': True,
        }
        return render(request, GENERIC_MESSAGE, data)
    analysis.delete()
    return redirect('cfd_profile_analysis_classic_view')


@login_required
def add_pta_analysis(request):
    if request.method == 'POST':
        form = PTAAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            return redirect('cfd_profile_analysis_pta_view')
    else:
        form = PTAAnalysisForm()
    data = {
        'forms': [form],
        'page_title': _('افزودن تحلیل PTA'),
        'form_cancel_url_name': 'cfd_profile_analysis_pta_view',
    }
    return render(request, GENERIC_MODEL_FORM, data)


@login_required
def add_classic_analysis(request):
    if request.method == 'POST':
        form = ClassicAnalysisForm(request.POST)
        if form.is_valid():
            analysis = form.save(commit=False)
            analysis.user = request.user
            analysis.save()
            if 'submit_and_signal' in request.POST:
                return redirect('cfd_profile_signals_add')
            return redirect('cfd_profile_analysis_classic_view')
    else:
        form = ClassicAnalysisForm()
    data = {
        'form': form,
        'action': 'cfd_profile_analysis_classic_add',
    }
    return render(request, CLASSIC_ANALYSIS_FORM_TEMPLATE, data)


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
            filled_signal = form.save(commit=False)
            filled_signal.status = Signal.SignalStatus.FILLED
            filled_signal.save()
            return redirect('cfd_profile_signals_month_view')
    else:
        form = FillSignalForm(instance=signal)
    context = {
        'forms': [form],
        'page_title': _('فرم پایان معامله'),
        'page_subtitle': _('سیگنال شماره ') + str(signal.id),
        'form_submit_url_name': 'cfd_profile_signals_fill',
        'form_submit_url_arg1': signal.id,
        'form_cancel_url_name': 'cfd_profile_signals_month_view',
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


@login_required
def cancel_signal(request, signal_id):
    signal = get_object_or_404(Signal, id=signal_id)
    if request.user != signal.user:
        return render(request, HTTP403PAGE)
    signal.status = Signal.SignalStatus.CANCELED
    signal.canceled_datetime = datetime.now()
    signal.save()
    return redirect('cfd_profile_signals_month_view')
